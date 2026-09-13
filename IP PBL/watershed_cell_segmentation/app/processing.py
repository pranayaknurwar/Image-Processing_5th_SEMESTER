import base64, cv2, numpy as np
from pathlib import Path
from skimage.metrics import structural_similarity as ssim

def b64(img, ext=".png"):
    ok, buf = cv2.imencode(ext, img)
    if not ok: raise ValueError("Could not encode image")
    return "data:image/png;base64," + base64.b64encode(buf).decode()

def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def add_noise(g, kind):
    if kind == "gaussian":
        noise = np.random.normal(0, 18, g.shape).astype(np.float32)
        return np.clip(g.astype(np.float32)+noise,0,255).astype(np.uint8)
    if kind == "salt_pepper":
        out=g.copy()
        rnd=np.random.random(g.shape)
        out[rnd<0.015]=0
        out[rnd>0.985]=255
        return out
    return g.copy()

def filter_image(g, kind, k):
    if kind == "mean": return cv2.blur(g,(k,k))
    if kind == "gaussian": return cv2.GaussianBlur(g,(k,k),0)
    return cv2.medianBlur(g,k)

def segmentation(filtered, threshold_mode, morph_mode):
    if threshold_mode == "otsu":
        _, binary = cv2.threshold(filtered,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    else:
        _, binary = cv2.threshold(filtered,127,255,cv2.THRESH_BINARY)
    # Assume bright cells on dark background; invert when background dominates.
    if np.mean(binary>0) > 0.65:
        binary = cv2.bitwise_not(binary)
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    op=cv2.MORPH_OPEN if morph_mode=="opening" else cv2.MORPH_CLOSE
    morph=cv2.morphologyEx(binary,op,kernel,iterations=1)

    dist=cv2.distanceTransform(morph,cv2.DIST_L2,5)
    if dist.max()>0:
        sure_fg=np.uint8(dist > 0.35*dist.max())*255
    else:
        sure_fg=np.zeros_like(morph)
    sure_bg=cv2.dilate(morph,kernel,iterations=2)
    unknown=cv2.subtract(sure_bg,sure_fg)
    n, markers=cv2.connectedComponents(sure_fg)
    markers=markers+1
    markers[unknown==255]=0

    color=cv2.cvtColor(filtered,cv2.COLOR_GRAY2BGR)
    markers=cv2.watershed(color,markers.astype(np.int32))
    boundary=color.copy()
    boundary[markers==-1]=[0,0,255]
    labels=np.unique(markers)
    cell_labels=[x for x in labels if x>1]
    count=len(cell_labels)
    marker_vis=np.zeros_like(filtered)
    for i,x in enumerate(cell_labels,1):
        marker_vis[markers==x]=min(255, 40+(i*37)%215)
    dist_vis=cv2.normalize(dist,None,0,255,cv2.NORM_MINMAX).astype(np.uint8)
    return binary,morph,dist_vis,marker_vis,boundary,count,markers

def metrics(ref, processed):
    a=ref.astype(np.float32); b=processed.astype(np.float32)
    mse=float(np.mean((a-b)**2))
    psnr=float("inf") if mse==0 else float(10*np.log10((255**2)/mse))
    score=float(ssim(ref,processed,data_range=255))
    return mse,psnr,score

def seg_metrics(pred, gt):
    pred=pred>0; gt=gt>0
    tp=np.logical_and(pred,gt).sum(); tn=np.logical_and(~pred,~gt).sum()
    fp=np.logical_and(pred,~gt).sum(); fn=np.logical_and(~pred,gt).sum()
    iou=tp/(tp+fp+fn) if tp+fp+fn else 1
    dice=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 1
    precision=tp/(tp+fp) if tp+fp else 1
    recall=tp/(tp+fn) if tp+fn else 1
    f1=2*precision*recall/(precision+recall) if precision+recall else 0
    acc=(tp+tn)/(tp+tn+fp+fn)
    return {k:round(float(v)*100,2) for k,v in dict(iou=iou,dice=dice,precision=precision,recall=recall,f1=f1,accuracy=acc).items()}

def process_image(image, params, folder):
    g=gray(image)
    noisy=add_noise(g,params["noise"])
    filt=filter_image(noisy,params["filter"],params["kernel"])
    binary,morph,dist,markers,boundary,count,_=segmentation(filt,params["threshold"],params["morph"])
    mse,psnr,ss=metrics(g,filt)
    return {
        "original":b64(g),"noisy":b64(noisy),"filtered":b64(filt),
        "threshold":b64(binary),"morphology":b64(morph),"distance":b64(dist),
        "markers":b64(markers),"segmented":b64(boundary),
        "cell_count":count,"mse":round(mse,4),
        "psnr":None if not np.isfinite(psnr) else round(psnr,4),"ssim":round(ss,4),
        "params":params,
        "segmentation_note":"Ground-truth metrics require a reference mask; PSNR/MSE/SSIM here measure image fidelity."
    }

def kernel_experiment(image, folder):
    results=[]
    g=gray(image)
    for k in [3,5,7,9]:
        noisy=g
        filt=filter_image(noisy,"median",k)
        _,_,_,_,_,count,_=segmentation(filt,"otsu","opening")
        mse,psnr,ss=metrics(g,filt)
        results.append({"kernel":f"{k}x{k}","psnr":None if not np.isfinite(psnr) else round(psnr,4),
                        "mse":round(mse,4),"ssim":round(ss,4),"cells":count})
    return {"results":results}
