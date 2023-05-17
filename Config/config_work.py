import configparser

class configWork:
    """Working with the config: change, read and etc."""


    def __init__(self, logger, config_path):
        """
        Connecting to the configparser.

        """
        
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.logger = logger 


    def changeValue(self, section, configuration, value):
        """
        Change the value of configutation.

        """        
        
        self.config.set(section, configuration, value)

        with open("config.ini", "w") as config_file:

            self.config.write(config_file)
            self.logger.info(f"Config: config {configuration} set to {value}.")
            
            return f"Конфигурации {configuration} установлено значение {value}."


    def readValue(self, section, value):
        """
        Read the value (value) in the section (section).

        """
        
        return self.config[section][value]