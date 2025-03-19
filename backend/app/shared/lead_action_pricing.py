LEAD_ACTION_COSTS = {
    "Website Visit": {
        "Visit": 1,
        "Click": 2,
        "Download": 3,
        "Form Submit": 5,
        "Purchase": 10,
    },
    "Social Media": {"Like": 2, "Follow": 3, "Share": 5, "Comment": 7, "Repost": 10},
    "Email Campaign": {"Open": 1, "Click": 15, "Unsubscribe": 5},
    "Referral": {"Signup": 20, "Purchase": 50},
    "Event": {"Attend": 2},
    "Webinar": {"Register": 5, "Attend": 10, "Follow-up": 5},
    "Demo Request": {"Submission": 10, "Follow-up": 5},
    "Trade Show": {"Visit": 5, "Follow-up": 10},
    "Conference": {"Attendance": 15, "Follow-up": 5},
    "Newsletter": {"Open": 1, "Click": 5},
    "Feedback": {"Submission": 10},
}

LEAD_VALUES = {"Website Visit": "1:10"}

ACTION_VALUES = {
    "LOW": [
        "LIKE",
        "OPEN",
        "ATTEND",
        "FOLLOW",
    ],
    "MEDIUM": ["CLICK", "VISIT", "REGISTER"],
    "HIGH": [
        "SUBMISSION",
        "ATTENDANCE",
    ],
}

ENGAGEMENT_MULTIPLIER = {"High": 5, "Medium": 3, "Low": 1}
