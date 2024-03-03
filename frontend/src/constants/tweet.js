import {
  roundCached,
  roundFavoriteBorder,
  roundIosShare,
  roundChatBubble,
} from "@quasar/extras/material-icons-round";
import {
  outlinedChatBubble,
  outlinedInsertPhoto,
  outlinedGifBox,
  outlinedPoll,
  outlinedSentimentSatisfied,
  outlinedEvent,
  outlinedAddLocation,
  outlinedLocationOn,
  outlinedVerified
} from "@quasar/extras/material-icons-outlined";

export const addTweetSelectOptions = [
  {
    label: "Everyone",
    value: "every",
    icon: "public"
  },
  {
    label: "Accounts you follow",
    value: "follower",
    icon: "how_to_reg"
  },
  {
    label: "Verified accounts",
    value: "follower",
    icon: outlinedVerified
  },
  {
    label: "Only accounts you mention",
    value: "mentionPeople",
    icon: "alternate_email",
  },
];


export const tweetFunctionButtons = [
  { label: 'reply', value: 'reply', icon: roundChatBubble, color: 'primary' },
  { label: 'repost', value: 'repost', icon: roundCached, color: 'cyan-7' },
  { label: 'like', value: 'like', icon: roundFavoriteBorder, color: 'pink-12' },
  { label: 'share', value: 'share', icon: roundIosShare, color: 'blue-6' },
]


export const addTweetFunctionButtons = [
  { label: "Photo", icon: outlinedInsertPhoto, value: "photo" },
  { label: "Gif", icon: outlinedGifBox, value: "gif" },
  { label: "Poll", icon: outlinedPoll, value: "poll" },
  { label: "Schedule", icon: outlinedEvent, value: "schedule" },
  { label: "Location", icon: outlinedLocationOn, value: "location" },
];

export const tweetReplyFunctionButtons = [
  { label: "Photo", icon: outlinedInsertPhoto, value: "photo" },
  { label: "Gif", icon: outlinedGifBox, value: "gif" },
  { label: "Emoji", icon: outlinedSentimentSatisfied, value: "emoji" },
  { label: "Location", icon: outlinedAddLocation, value: "location" },
];
