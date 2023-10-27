import requests
from bs4 import BeautifulSoup
import json


# Function to scrape comments from a given issue URL
def scrape_comments(issue_url):
    comments_data = []
    response = requests.get(issue_url)
    soup = BeautifulSoup(response.text, "html.parser")
    comments = soup.find_all("div", class_="timeline-comment-wrapper timeline-new-comment")

    for comment in comments:
        commenter_name = comment.find("span", class_="author").text.strip()
        comment_text = comment.find("div", class_="edit-comment-hide").text.strip()
        comments_data.append({"commenter_name": commenter_name, "comment_text": comment_text})

    return comments_data


# Function to scrape issues from a given URL
def scrape_github_issues(url, sl):
    issues_data = []
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        issues = soup.find_all("div", class_="js-navigation-container js-active-navigation-container")[0]

        for index, issue in enumerate(issues.find_all("div", class_="js-navigation-item")):
            issue_details = {"index": sl}
            sl += 1

            print(f"Working on {sl}th issue")

            issue_details["date"] = issue.find("relative-time").text.strip()
            issue_details["title"] = issue.find("a").text.strip()
            issue_details["url"] = "https://github.com" + issue.find("a")["href"].strip()

            # Extract poster's name
            poster_name = issue.find("span", class_="opened-by").text.strip()
            issue_details["poster_name"] = poster_name

            # Fetch detailed issue description
            issue_response = requests.get(issue_details["url"])
            issue_soup = BeautifulSoup(issue_response.text, "html.parser")
            issue_details["description"] = issue_soup.find("div", class_="edit-comment-hide").text.strip()

            # Scrape comments for this issue
            issue_details["comments"] = scrape_comments(issue_details["url"])

            issues_data.append(issue_details)

        # Check if there is a next page of issues
        next_page = soup.find("a", class_="next_page")
        if next_page:
            url = "https://github.com" + next_page["href"]
        else:
            url = None

    return issues_data


def createDataset(repo_link):
    # URLs of the GitHub issues pages for open and closed issues
    open_issues_url = repo_link + "/issues?q=is%3Aissue+is%3Aopen"
    # closed_issues_url = repo_link + "/issues?q=is%3Aissue+is%3Aclosed"
    sl_number = 0
    # Scrape open issues and comments
    open_issues_data = scrape_github_issues(open_issues_url, sl_number)
    # Scrape closed issues and comments
    # closed_issues_data = scrape_github_issues(closed_issues_url, len(open_issues_data))
    # Combine open and closed issues data
    # all_issues_data = open_issues_data + closed_issues_data
    all_issues_data = open_issues_data
    # Store data in JSON format
    return all_issues_data


# createDataset()
