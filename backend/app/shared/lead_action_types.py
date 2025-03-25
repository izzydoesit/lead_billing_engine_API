from enum import Enum


# ENGAGEMENT LEVEL
class EngagementLevelTypes(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# LEAD TYPES
class LeadTypes(str, Enum):
    WEBSITE_VISIT = "Website Visit"
    SOCIAL_MEDIA = "Social Media"
    EMAIL_CAMPAIGN = "Email Campaign"
    REFERRAL = "Referral"
    EVENT = "Event"
    WEBINAR = "Webinar"
    DEMO_REQUEST = "Demo Request"
    TRADE_SHOW = "Trade Show"
    CONFERENCE = "Conference"
    NEWSLETTER = "Newsletter"
    FEEDBACK = "Feedback"


# ACTION TYPES
class ActionTypes(str, Enum):
    VISIT = "Visit"
    DOWNLOAD = "Download"
    FORM_SUBMIT = "Form Submit"
    PURCHASE = "Purchase"
    LIKE = "Like"
    FOLLOW = "Follow"
    SHARE = "Share"
    COMMENT = "Comment"
    REPOST = "Repost"
    OPEN = "Open"
    CLICK = "Click"
    UNSUBSCRIBE = "Unsubscribe"
    SIGNUP = "Signup"
    REGISTER = "Register"
    ATTEND = "Attend"
    FOLLOW_UP = "Follow-up"
    ATTENDANCE = "Attendance"
    SUBMISSION = "Submission"


class BillableStatus(str, Enum):
    BILLED = "Billed"
    NOT_BILLED = "Not Billed (Duplicate)"
