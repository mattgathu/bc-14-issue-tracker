from issuetracker import models
import random

TITLES = ["Low Salary Allowance", "High Maintenace Cost", "Noisy Workplace",
          "Entertainment Allowance", "Overtime Work", "Better meals", "Research Budget",
          "Power cuts", "Slow Internet"]
DESC = """Emmentaler or Emmental is a yellow, medium-hard cheese that originated in the area around
Emmental, Switzerland. It is one of the cheeses of Switzerland, and is sometimes known as Swiss
cheese."""
DESC2 = """Church is definitely on the move and now we took it up to the cathedral cause the "-ism" is enormous, you know what I'm talking 'bout?
We out here rotating under the five P's, proper preparation prevents poor performance
Know what I'm talking 'bout?"""
DEPARTMENTS = ["Finance", "Operations", "Sales", "Production", "Success"]
PRIORITY = ["low", "medium", "high"]

for _ in range(1):
    for title in TITLES:
        summary = title
        desc = random.choice([DESC, DESC2])
        status = random.choice(["open", "closed"])
        depart = random.choice(DEPARTMENTS)
        priority = random.choice(PRIORITY)
        prog = random.choice([True, False])
        data = {
            "summary": summary,
            "description": desc,
            "status": status,
            "department": depart,
            "priority": priority,
            "in_progress": prog,
            "user_id": 3
        }
        issue = models.Issue(**data)
        issue.save()
        print(issue.summary)
