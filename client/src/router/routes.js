const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import("src/pages/LoginPage.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("src/pages/SignUpPage.vue"),
  },
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        component: () => import("src/pages/HomePage.vue"),
      },
      { path: "explore", component: () => import("src/pages/ExplorePage.vue") },
      { path: "notifications", component: () => import("src/pages/NotificationsPage.vue") },
      { path: "messages", component: () => import("src/pages/MessagesPage.vue") },
      { path: "lists", component: () => import("src/pages/ListsPage.vue") },
      { path: "bookmarks", component: () => import("src/pages/BookmarksPage.vue") },
      { path: "profile", component: () => import("src/pages/ProfilePage.vue") },
      // { path: "trends", component: () => import("src/pages/others/TrendShowMore.vue") },
      // { path: "search", component: () => import("src/pages/explore/SearchResult.vue") },
      // { path: "user", component: () => import("src/pages/others/UserProfile.vue") },
      { path: "tweet", component: () => import("src/pages/PostDetailPage.vue") },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
