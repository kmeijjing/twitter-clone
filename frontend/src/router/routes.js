

const routes = [
  {
    path: "/auth",
    component: () => import("layouts/AuthLayout.vue"),
    meta: {
      unauthenticated: true,
    },
    children: [
      {
        path: "",
        name: "SignIn",
        component: () => import("src/pages/LoginPage.vue"),
      },
      {
        path: "signup",
        name: "SignUp",
        component: () => import("src/pages/SignUpPage.vue"),
      },
      {
        path: "signup-success",
        name: "SignUpSuccess",
        component: () => import("src/pages/SignUpResultPage.vue"),
      },
    ]
  },
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    meta: {
      authenticated: true,
    },
    children: [
      {
        path: "",
        name: "Home",
        component: () => import("src/pages/HomePage.vue"),
      },
      {
        path: "explore",
        component: () => import("src/pages/ExplorePage.vue")
      },
      {
        path: "notifications",
        component: () => import("src/pages/NotificationsPage.vue")
      },
      {
        path: "messages",
        component: () => import("src/pages/MessagesPage.vue")
      },
      {
        path: "lists",
        component: () => import("src/pages/ListsPage.vue")
      },
      {
        path: "bookmarks",
        component: () => import("src/pages/BookmarksPage.vue")
      },
      {
        path: "profile",
        name: "MyProfile",
        component: () => import("src/pages/MyProfilePage.vue")
      },
      {
        path: "profile/:userId",
        name: "OtherProfile",
        component: () => import("src/pages/OtherProfilePage.vue")
      },
      {
        path: "trends",
        name: "Trends",
        component: () => import("src/pages/TrendsPage.vue")
      },
      {
        path: "search/:keyword",
        name: "Search",
        component: () => import("src/pages/SearchResultPage.vue")
      },
      {
        path: "post/:id",
        name: "Post",
        component: () => import("src/pages/PostDetailPage.vue")
      },
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
