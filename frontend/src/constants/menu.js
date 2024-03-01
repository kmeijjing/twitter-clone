import {
  outlinedHome,
  outlinedSearch,
  outlinedNotificationsNone,
  outlinedMailOutline,
  outlinedBookmarkBorder,
  outlinedSummarize,
  outlinedPersonOutline,
  outlinedMoreHoriz,
} from "@quasar/extras/material-icons-outlined";

export const linksList = [
  {
    title: "home",
    icon: outlinedHome,
    activeIcon: "home",
    link: "/",
  },
  {
    title: "explore",
    icon: outlinedSearch,
    activeIcon: "search",
    link: "/explore",
  },
  {
    title: "notifications",
    icon: outlinedNotificationsNone,
    activeIcon: "notifications",
    link: "/notifications",
  },
  {
    title: "messages",
    icon: outlinedMailOutline,
    activeIcon: "mail",
    link: "/messages",
  },
  {
    title: "lists",
    icon: outlinedSummarize,
    activeIcon: "summarize",
    link: "/lists",
  },
  {
    title: "bookmarks",
    icon: outlinedBookmarkBorder,
    activeIcon: "bookmark",
    link: "/bookmarks",
  },
  {
    title: "profile",
    icon: outlinedPersonOutline,
    activeIcon: "person",
    link: "/profile",
  },
  {
    title: "more",
    icon: outlinedMoreHoriz,
    activeIcon: "moreHoriz",
    link: "",
  },
];

export default linksList;
