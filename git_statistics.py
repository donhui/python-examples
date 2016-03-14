# -*- coding: utf-8 -*-
import os


def get_repo_name(git_path):
    repo_name = git_path.replace("\\", "/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name.rstrip(".git")
    return repo_name


# 生成某个时间段内的git log记录（xml格式）
def generate_log_filter_by_date(git_path, start_date, end_date, log_output_file):
    os.chdir(git_path)
    git_log_cmd = 'git log --pretty=format:"%h %aE %s" --since={' + start_date + '} --until={' + end_date + '}>' + log_output_file
    print git_log_cmd
    os.system(git_log_cmd)
    return log_output_file


def get_commits_and_authors_by_log(log_output_file):
    commits_list = []
    commits_without_merge_list = []
    author_list = []
    with open(log_output_file) as f:
        for line in f:
            commit_message = line.split(" ")[2]
            commit_sha = line.split(" ")[0]
            author = line.split(" ")[1]
            commits_list.append(commit_sha)
            author_list.append(author)
            if not commit_message.startswith("Merge"):
                commits_without_merge_list.append(commit_sha)
    return commits_list, set(author_list), commits_without_merge_list


def generate_diff_by_commits_list(git_path, commits_list, diff_file):
    if os.path.exists(diff_file):
        os.remove(diff_file)
    os.chdir(git_path)
    print os.getcwd()
    for commit in commits_list:
        git_show_commit_diff = "git show %s --no-renames -p>>%s" % (commit, diff_file)
        os.system(git_show_commit_diff)
    return diff_file


# 从diff中获取删除行数、添加行数
def get_additions_deletions_from_diff(diff_file):
    files_change_num = 0
    additions_num = 0
    deletions_num = 0
    with open(diff_file) as f:
        for line in f.readlines():
            if line.startswith("-") and not line.startswith("---"):
                deletions_num += 1
            elif line.startswith("+") and not line.startswith("+++"):
                additions_num += 1
            elif line.startswith("index") and not (line.endswith(".class") or line.endswith(".jar")):
                files_change_num += 1
    return files_change_num, additions_num, deletions_num


def get_all_info(git_path, start_date, end_date):
    repo_name = get_repo_name(git_path)
    log_output_file_name = repo_name + '_' + start_date + '_' + end_date + '-log.xml'
    log_output_file = os.path.join(current_dir, log_output_file_name)
    diff_file_name = repo_name + '_' + start_date + '_' + end_date + '.diff'
    diff_file = os.path.join(current_dir, diff_file_name)
    log_output_file = generate_log_filter_by_date(git_path, start_date, end_date, log_output_file)
    commits, authors, commits_without_merge = get_commits_and_authors_by_log(log_output_file)
    commits_number = len(commits)
    generate_diff_by_commits_list(git_path, commits_without_merge, diff_file)
    files_change_num, additions_num, deletions_num = get_additions_deletions_from_diff(diff_file)
    print "git仓库" + repo_name + "从" + start_date + "到" + end_date + "统计信息如下："
    print "提交人员数:" + str(len(authors))
    print "提交次数:" + str(commits_number)
    print "变动文件数:" + str(files_change_num)
    print "总修改行:" + str(additions_num + deletions_num)
    print "增加行数:" + str(additions_num)
    print "删除行数:" + str(deletions_num)
    return


if __name__ == "__main__":
    current_dir = os.getcwd()
    git_local_path = 'D:\data\git-data/repositories/namespace/xxx.git'

    start_date_151001 = '2015-10-01'
    end_date_151101 = '2015-11-01'
    get_all_info(git_local_path, start_date_151001, end_date_151101)
