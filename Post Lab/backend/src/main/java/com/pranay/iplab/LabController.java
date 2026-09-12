package com.pranay.iplab;
import org.springframework.web.bind.annotation.*;
import java.util.*;
@RestController @RequestMapping("/api")
public class LabController {
 private final ExperimentRunRepository repo;
 LabController(ExperimentRunRepository repo){this.repo=repo;}
 @GetMapping("/student") public Map<String,String> student(){return Map.of("name","Pranay Aknurwar","branch","Computer Science And Engineering","year","3rd","rollNo","CS24099","subject","Image Processing Lab");}
 @GetMapping("/experiments") public List<Map<String,String>> experiments(){
  String[][] a={{"1","Prelab / Setup"},{"2","RGB, Grayscale & Operations"},{"3","Geometric Transformations"},{"4","Image Enhancement"},{"5","Spatial Domain Filters"},{"6","Image Inpainting"},{"7","Lossless Compression"},{"8","Morphological Operations"},{"9","Correlation Object Detection"},{"10","Colour Spaces"},{"11","Edge Detection"}};
  List<Map<String,String>> out=new ArrayList<>(); for(String[] x:a) out.add(Map.of("code",x[0],"name",x[1])); return out;
 }
 @GetMapping("/runs") public List<ExperimentRun> runs(){return repo.findAll();}
 @PostMapping("/runs") public ExperimentRun run(@RequestBody Map<String,String> b){return repo.save(new ExperimentRun(b.get("experimentCode"),b.get("operation"),b.get("imageName")));}
}