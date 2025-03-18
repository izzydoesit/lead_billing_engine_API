from multiprocessing.context import _LockLike
from Pydantic import Enum


class EngagementLevelTypes(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class LeadTypes(Enum):
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


class ActionTypes(Enum):
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
    PURCHASE = "Purchase"
    REGISTER = "Register"
    ATTEND = "Attend"
    FOLLOW_UP = "Follow-up"
    SUBMISSION = "Submission"
    VISIT = "Visit"
    ATTENDANCE = "Attendance"
    OPEN = "Open"
    SUBMISSION = "Submission"
