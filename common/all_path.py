import os

base_path = os.path.dirname(os.path.dirname(__file__))
# base
appPath = os.path.join(base_path, 'app')
dataPath = os.path.join(base_path, 'data')
logPath = os.path.join(base_path,  'logs')
picturePath = os.path.join(base_path, 'png')
screenPath = os.path.join(base_path,  'screencap')

# config
configPath = os.path.join(base_path, 'config')
images_Path=os.path.join(configPath,"png")
environmentPath=os.path.join(configPath,"environment.properties")

# target报告
targetPath=os.path.join(base_path, 'target')
reportsPath = os.path.join(targetPath, 'allure-report')
allure_results = os.path.join(targetPath, 'allure-results')


if __name__ == "__main__":
    print("base_path is {}".format(base_path))