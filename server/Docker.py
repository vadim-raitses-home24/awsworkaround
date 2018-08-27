import subprocess


class Docker:

    def get_repository(self):
        subprocess.run(["git", "pull"])

        pass
    def build_docker(self):
        pass
    def upload_docker(self):
        pass


    def main(self):
        print("start")
        self.get_repository()
        pass

if __name__ == "__main__":
    Docker().main()