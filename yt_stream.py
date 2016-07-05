#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of  https://cloud.google.com/console
DEVELOPER_KEY = "Your key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term. With DEVELOPER_KEY only 2 per HTTP request.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=50  #max value for use with DEVELOPER_KEY
  ).execute()

  videos = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s) (%s) (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"],
                                 search_result["snippet"]["channelId"],
                                 search_result["snippet"]["publishedAt"]))

  print "Videos:\n", "\n".join(videos), "\n"


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)