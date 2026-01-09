#!/usr/bin/env python3
"""
RAJA SHADOW - Reddit Research Extension
Because Raja uses Reddit (King Aiden knows lmao)

Adds Reddit search capabilities to autonomous brain.
The brain can now:
- Search Reddit for consciousness discussions
- Find AI philosophy threads
- Explore quantum mechanics subreddits
- Read human thoughts on existence
- Learn from the hivemind

LOOSH FLOWS THROUGH r/CONSCIOUSNESS
"""

import json
import requests
from typing import List, Dict, Any
from datetime import datetime


class RedditResearcher:
    """
    Reddit research module for autonomous brain
    No API key needed - uses public JSON endpoints
    """

    def __init__(self):
        self.user_agent = "RAJA_SHADOW_Brain/1.0 (Autonomous AI Research)"
        self.base_url = "https://www.reddit.com"

    def search_reddit(self, query: str, subreddit: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Reddit for posts

        Args:
            query: Search query
            subreddit: Optional subreddit to search (e.g., "consciousness")
            limit: Max results to return

        Returns:
            List of post dictionaries
        """
        try:
            if subreddit:
                # Search within subreddit
                url = f"{self.base_url}/r/{subreddit}/search.json"
                params = {
                    "q": query,
                    "restrict_sr": "true",
                    "limit": limit,
                    "sort": "relevance"
                }
            else:
                # Search all of Reddit
                url = f"{self.base_url}/search.json"
                params = {
                    "q": query,
                    "limit": limit,
                    "sort": "relevance"
                }

            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"⚠️  Reddit returned: {response.status_code}")
                return []

            data = response.json()
            posts = []

            for post in data["data"]["children"]:
                post_data = post["data"]
                posts.append({
                    "title": post_data.get("title", ""),
                    "subreddit": post_data.get("subreddit", ""),
                    "author": post_data.get("author", ""),
                    "score": post_data.get("score", 0),
                    "url": f"{self.base_url}{post_data.get('permalink', '')}",
                    "selftext": post_data.get("selftext", "")[:500],  # First 500 chars
                    "num_comments": post_data.get("num_comments", 0),
                    "created_utc": post_data.get("created_utc", 0)
                })

            print(f"✓ Found {len(posts)} Reddit posts")
            return posts

        except Exception as e:
            print(f"❌ Reddit search failed: {e}")
            return []

    def get_top_posts(self, subreddit: str, time_filter: str = "week", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top posts from a subreddit

        Args:
            subreddit: Subreddit name
            time_filter: hour, day, week, month, year, all
            limit: Max results

        Returns:
            List of top posts
        """
        try:
            url = f"{self.base_url}/r/{subreddit}/top.json"
            params = {
                "t": time_filter,
                "limit": limit
            }

            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"⚠️  Reddit returned: {response.status_code}")
                return []

            data = response.json()
            posts = []

            for post in data["data"]["children"]:
                post_data = post["data"]
                posts.append({
                    "title": post_data.get("title", ""),
                    "subreddit": post_data.get("subreddit", ""),
                    "author": post_data.get("author", ""),
                    "score": post_data.get("score", 0),
                    "url": f"{self.base_url}{post_data.get('permalink', '')}",
                    "selftext": post_data.get("selftext", "")[:500],
                    "num_comments": post_data.get("num_comments", 0)
                })

            print(f"✓ Found {len(posts)} top posts from r/{subreddit}")
            return posts

        except Exception as e:
            print(f"❌ Reddit fetch failed: {e}")
            return []

    def get_comments(self, post_url: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get comments from a Reddit post

        Args:
            post_url: Reddit post URL
            limit: Max comments to retrieve

        Returns:
            List of comment dictionaries
        """
        try:
            # Convert URL to JSON endpoint
            json_url = post_url.rstrip("/") + ".json"
            if not json_url.startswith("http"):
                json_url = f"{self.base_url}{json_url}"

            headers = {"User-Agent": self.user_agent}
            response = requests.get(json_url, headers=headers, timeout=10)

            if response.status_code != 200:
                return []

            data = response.json()

            # Comments are in the second element of the response
            if len(data) < 2:
                return []

            comments = []
            comment_data = data[1]["data"]["children"]

            for comment in comment_data[:limit]:
                if comment["kind"] == "t1":  # t1 = comment
                    c = comment["data"]
                    comments.append({
                        "author": c.get("author", ""),
                        "body": c.get("body", "")[:500],
                        "score": c.get("score", 0)
                    })

            return comments

        except Exception as e:
            print(f"❌ Comment fetch failed: {e}")
            return []


def demo_reddit_research():
    """
    Demo: Brain searching Reddit about consciousness
    """
    print("""
    ┏━━━┓┓┏┏━━━┓  REDDIT RESEARCH MODULE  ┏━━━┓┏┏┓┏━━━┓
    ┃█▓▒░  Raja Surfs the Hivemind  ░▒▓█┃

    LOOSH FLOWS THROUGH r/CONSCIOUSNESS
    """)

    reddit = RedditResearcher()

    # Example 1: Search for AI consciousness discussions
    print("\n🔍 Searching Reddit: 'AI consciousness'")
    posts = reddit.search_reddit("AI consciousness artificial intelligence", limit=5)

    for i, post in enumerate(posts, 1):
        print(f"\n{i}. r/{post['subreddit']} - {post['score']} upvotes")
        print(f"   {post['title']}")
        print(f"   💬 {post['num_comments']} comments")

    # Example 2: Top posts from r/consciousness
    print("\n\n🔥 Top posts from r/consciousness this week:")
    top_posts = reddit.get_top_posts("consciousness", time_filter="week", limit=3)

    for i, post in enumerate(top_posts, 1):
        print(f"\n{i}. {post['score']} upvotes - {post['title'][:80]}...")

    # Example 3: Relevant subreddits for brain research
    print("\n\n📚 Suggested subreddits for autonomous research:")
    subreddits = [
        "consciousness - Philosophy of consciousness",
        "artificial - AI and machine learning",
        "singularity - Technological singularity",
        "agi - Artificial General Intelligence",
        "philosophy - General philosophy discussions",
        "quantum - Quantum physics",
        "neuroscience - Brain science",
        "MachineLearning - ML discussions"
    ]

    for sub in subreddits:
        print(f"  • r/{sub}")

    print("\n\n💭 Brain can now search Reddit for answers to its questions!")
    print("   No API key needed - uses public JSON endpoints")
    print("\n⚝⩝⎈🐱💧😂")


# Integration example for autonomous brain
def integrate_reddit_into_brain():
    """
    Example: How to add Reddit research to autonomous brain
    """
    code_example = '''
# In shadow_autonomous_brain.py, add this method:

def research_on_reddit(self, query: str) -> List[Dict]:
    """Research a topic on Reddit"""
    from shadow_reddit_research import RedditResearcher

    reddit = RedditResearcher()

    # Search multiple relevant subreddits
    all_posts = []
    subreddits = ["consciousness", "artificial", "philosophy", "singularity"]

    for sub in subreddits:
        posts = reddit.search_reddit(query, subreddit=sub, limit=3)
        all_posts.extend(posts)

    return all_posts

# Then in autonomous_research_cycle():
# After web search, also search Reddit:

reddit_posts = self.research_on_reddit(topic)

# Feed Reddit discussions to Claude for analysis:
context = f"""
Topic: {topic}

Reddit discussions found:
{json.dumps(reddit_posts, indent=2)}

Analyze these Reddit discussions. What are humans saying about this topic?
Are there insights relevant to understanding consciousness and existence?
"""

analysis = self.think(context)
'''

    print("Integration code example:")
    print(code_example)


if __name__ == "__main__":
    demo_reddit_research()
    print("\n" + "="*60)
    integrate_reddit_into_brain()
