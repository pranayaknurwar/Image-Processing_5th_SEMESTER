from pathlib import Path
import cv2, numpy as np

out=Path("sample_data"); out.mkdir(exist_ok=True)
rng=np.random.default_rng(7)
for idx in range(1,6):
    h,w=420,560
    img=np.zeros((h,w),np.uint8)
    n=22+idx*4
    for _ in range(n):
        cx=int(rng.integers(35,w-35)); cy=int(rng.integers(35,h-35))
        r=int(rng.integers(14,30))
        cv2.circle(img,(cx,cy),r,int(rng.integers(150,245)),-1)
    img=cv2.GaussianBlur(img,(5,5),0)
    if idx==2: img=np.clip(img.astype(np.float32)*0.65+20,0,255).astype(np.uint8)
    if idx==3: img=np.clip(img.astype(np.float32)+rng.normal(0,24,img.shape),0,255).astype(np.uint8)
    if idx==4:
        for x in range(100,470,55): cv2.circle(img,(x,210),28,220,-1)
    if idx==5:
        for x,y in [(170,180),(205,200),(235,175),(300,230),(330,205),(360,235)]: cv2.circle(img,(x,y),32,220,-1)
    cv2.imwrite(str(out/f"cell_image_{idx}.png"),img)
    cv2.imwrite(str(out/f"cell_mask_{idx}.png"),(img>80).astype(np.uint8)*255)
print("Created 5 sample images and masks in sample_data/")
