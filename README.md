# CI-CD Pipeline, Provisioning and Maintenance components for FitNesse Testautomation

## Dependencies
Check requirements.txt

## Checks after installation


## License

MIT

## Principles

### deploy lists

* All components expect a deploylist text file as input. You should keep deploylists in your source code Git. Suggested location:
<root>/<feature>/config/<deploylist> where <root> is the base location within your Git, <feature> is your submodule (if any), and <deploylist> is the text file that contains the items to be deployed.
  For example:
  <myGit>/demo/config/fitnesse_deploylist.txt
  <myGit>/demo/config/infa_deploylist.txt

### environment variables

* The python scripts use environment variables to determine locations, features and many other parameters. The environment variables that can or at times must be set can be found in:
  * generalSettings: log directory, artifact directory, configuration directory and more

## Examples

Check the examples folder in the Git repository devops-informatica-tools for more info on the structure of deploy lists.

### Run from python3 command line
````
$ python3
>>> from create_fitnesse_artifact import createFitNesseArtifact
>>> a=createFitNesseArtifact.CreateFitNesseArtifact([])
>>> result=a.runit(a.arguments)
>>> quit()


$ ls -l *CreateFitNesseArtifact.log
-rw-r--r--   1 jacbeekers  staff   2305 Jun  8 18:38 20200608-183831.984799-CreateFitNesseArtifact.log

$ more 20200608-183831.984799-CreateFitNesseArtifact.log 
2020-06-08 18:38:37,801 - create_fitnesse_artifact.createFitNesseArtifact - DEBUG - runit - Started
2020-06-08 18:38:37,801 - create_fitnesse_artifact.createFitNesseArtifact - DEBUG - runit - logDir is >.<.
2020-06-08 18:38:37,801 - supporting.generalSettings - DEBUG - getenvvars - started
2020-06-08 18:38:37,801 - supporting.generalSettings - DEBUG - getenvvars - logDir set to >.<.
2020-06-08 18:38:37,801 - supporting.generalSettings - DEBUG - getenvvars - resultDir set to >.<.
2020-06-08 18:38:37,801 - supporting.generalSettings - DEBUG - getenvvars - artifactDir set to >.<.
2020-06-08 18:38:37,801 - supporting.generalSettings - DEBUG - getenvvars - configDir set to >.<.
2020-06-08 18:38:37,802 - supporting.generalSettings - DEBUG - getenvvars - sourceDir set to >.<.
2020-06-08 18:38:37,802 - supporting.generalSettings - DEBUG - getenvvars - releaseID set to >0.1<.
2020-06-08 18:38:37,802 - supporting.generalSettings - DEBUG - getenvvars - do_not_run set to >False<.
2020-06-08 18:38:37,802 - supporting.generalSettings - DEBUG - getenvvars - completed
2020-06-08 18:38:37,802 - create_fitnesse_artifact.helpers.fitnesseSettings - DEBUG - getfitnesseenvvars - started
2020-06-08 18:38:37,802 - create_fitnesse_artifact.helpers.fitnesseSettings - INFO - outfitnesseenvvars - fitnessedeploylist is >./fitnesse_deploylist.txt<.
2020-06-08 18:38:37,802 - create_fitnesse_artifact.helpers.fitnesseSettings - INFO - outfitnesseenvvars - sourcefitnessedir is >./.<.
2020-06-08 18:38:37,802 - create_fitnesse_artifact.helpers.fitnesseSettings - INFO - outfitnesseenvvars - targetfitnessedir is >./.<.
2020-06-08 18:38:37,802 - create_fitnesse_artifact.helpers.fitnesseArtifactChecks - DEBUG - fitnesseartifactchecks - started
2020-06-08 18:38:37,802 - create_fitnesse_artifact.helpers.fitnesseArtifactChecks - WARNING - fitnesseartifactchecks - fitnessedeploylist is >./fitnesse_deploylist.txt<. Deploylist not found - FitNesse artifact IGNORED.
2020-06-08 18:38:37,802 - create_fitnesse_artifact.helpers.fitnesseArtifactChecks - DEBUG - fitnesseartifactchecks - completed with >-1<.
2020-06-08 18:38:37,802 - root - WARNING - runit - Artifact ignored.
2020-06-08 18:38:37,802 - create_fitnesse_artifact.createFitNesseArtifact - DEBUG - runit - Completed with return code >0< and result code >0<.
```





