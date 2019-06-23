from datetime import datetime
import os

def current_time_str():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def project_home():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def tmp_dir():
    return os.path.join(project_home(), 'data/tmp')

if __name__ == '__main__':
    print(project_home())
