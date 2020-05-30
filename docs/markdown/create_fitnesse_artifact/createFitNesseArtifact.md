Module create_fitnesse_artifact.createFitNesseArtifact
======================================================
.. versionchanged:: 20200530.0
    * moved FitNesse to its own package
    * changes due to logging module changes
    * documentation

Classes
-------

`CreateFitNesseArtifact(argv, log_on_console=True)`
:   

    ### Methods

    `parse_the_arguments(self, arguments)`
    :   Parses the provided arguments and exits on an error.
        Use the option -h on the command line to get an overview of the required and optional arguments.
        
        Args:
            arguments: List containing command line arguments
        
        Returns:
            A list with validated command line arguments

    `runit(self, arguments)`
    :   Creates a FitNesse artifact, consisting on collected test directories and files
        It uses a deploy list that contains subdirectories.
        Module uses environment variables that steer the artifact creation.
        
        Args:
            arguments: The command line arguments (none actually at the moment)