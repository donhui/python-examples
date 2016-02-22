from jenkinsapi.jenkins import Jenkins

jenkins_url = "http://xxx:8080"
jenkins_username = "user"
jenkins_password = "pass"


def get_server_instance():
    server = Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
    return server


def delete_all_jobs():
    server = get_server_instance()
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        print 'Removing Job:%s' % job_instance.name
        server.delete_job(job_instance.name)
if __name__ == "__main__":
    delete_all_jobs()
