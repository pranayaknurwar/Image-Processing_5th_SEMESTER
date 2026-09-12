package com.pranay.iplab;
import jakarta.persistence.*;
import java.time.Instant;
@Entity @Table(name="experiment_runs")
public class ExperimentRun {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
 private String experimentCode; private String operation; private String imageName; private Instant performedAt;
 public ExperimentRun() {}
 public ExperimentRun(String c,String o,String n){experimentCode=c;operation=o;imageName=n;performedAt=Instant.now();}
 public Long getId(){return id;} public String getExperimentCode(){return experimentCode;}
 public String getOperation(){return operation;} public String getImageName(){return imageName;} public Instant getPerformedAt(){return performedAt;}
}