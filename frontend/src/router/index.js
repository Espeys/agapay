import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store";
Vue.use(VueRouter);

const isAuthenticatedGuard = (to, from, next) => {
  if (store.getters["auth/isAuthenticated"]) next();
  else next({ name: "Public Newsfeed" });
};

const isAuthenticatedProviderGuard = (to, from, next) => {
  if (store.getters["auth/isAuthenticated"]) {
    if (
      store.getters["auth/group"] === "provider" ||
      store.getters["auth/group"] === "organization"
    )
      next();
    else next({ name: "Home" });
  } else next({ name: "Public Newsfeed" });
};

const isAuthenticatedRegularGuard = (to, from, next) => {
  if (store.getters["auth/isAuthenticated"]) {
    if (store.getters["auth/group"] === "regular") next();
    else next({ name: "Home" });
  } else next({ name: "Public Newsfeed" });
};

const routes = [
  {
    path: "",
    children: [
      {
        path: "",
        name: "Home",
        component: () => import("@/views/Home/Home.vue"),
        beforeEnter: isAuthenticatedGuard
      },
      {
        path: "promotions",
        name: "Public Newsfeed",
        component: () =>
          import("@/views/public/PublicNewsFeed/PublicNewsFeed.vue")
      },
      {
        path: "post/:slug",
        name: "Post Details",
        component: () => import("@/views/public/PostDetails/PostDetails.vue"),
        props: true
      },
      {
        path: "post",
        name: "Post Creation",
        component: () => import("@/views/CreateEditPost/CreateEditPost.vue"),
        beforeEnter: isAuthenticatedGuard
      },

      {
        path: "saved",
        name: "Saved",
        component: () => import("@/views/SavedPost/SavedPost.vue"),
        beforeEnter: isAuthenticatedGuard
      },
      {
        path: "search",
        name: "Search",
        component: () => import("@/views/Search/Search.vue"),
        beforeEnter: isAuthenticatedGuard
      },
      {
        path: "providers",
        name: "Service Providers",
        component: () => import("@/views/ServiceProviders/ServiceProviders.vue")
      },
      {
        path: "connections",
        name: "Connections",
        component: () =>
          import("@/views/providers/Connections/Connections.vue"),
        beforeEnter: isAuthenticatedProviderGuard
      },
      {
        path: "community",
        name: "Community Help",
        component: () => import("@/views/CommunityHelp/CommunityHelp.vue"),
        beforeEnter: isAuthenticatedGuard
      },
      {
        path: "information",
        name: "Emotional Mental Health",
        component: () =>
          import("@/views/EmotionalMentalHealth/EmotionalMentalHealth.vue"),
        beforeEnter: isAuthenticatedGuard
      },
      {
        path: "diary",
        name: "Mood Tracking",
        component: () =>
          import("@/views/regular/MoodTracking/MoodTracking.vue"),
        beforeEnter: isAuthenticatedRegularGuard
      },
      {
        path: "assessment",
        name: "Self-Assessment Test",
        component: () =>
          import("@/views/regular/SelfAssessmentTest/SelfAssessmentTest.vue"),
        beforeEnter: isAuthenticatedRegularGuard
      },
      {
        path: "profile/:slug",
        name: "User Profile",
        props: true,
        component: () => import("@/views/Profile/Profile.vue"),
        beforeEnter: isAuthenticatedGuard
      },
      {
        path: "profile",
        name: "Profile",
        component: () => import("@/views/Profile/Profile.vue"),
        beforeEnter: isAuthenticatedGuard
      },
      {
        path: "messages",
        name: "Messages",
        component: () => import("@/views/Messages/Messages.vue"),
        beforeEnter: isAuthenticatedGuard
      },
      {
        path: "settings",
        name: "Settings",
        component: () => import("@/views/Settings/Settings.vue"),
        beforeEnter: isAuthenticatedGuard
      },
      {
        path: "notification",
        name: "Notification",
        component: () => import("@/views/mobile/Notification/Notification.vue"),
        beforeEnter: isAuthenticatedGuard
      },
      {
        path: "navigation",
        name: "Navigation",
        component: () => import("@/views/mobile/Navigation/Navigation.vue"),
        beforeEnter: isAuthenticatedGuard
      }
    ],
    component: () => import("@/pages/AccountPage/AccountPage.vue"),
    beforeEnter: async (to, from, next) => {
      if (store.getters["auth/isAuthenticated"]) {
        await store.dispatch("auth/setAccess");

        const { slug } = store.state.auth.user;
        const ownData = true;

        await store.dispatch("profile/getUserFollower", { slug, ownData });
        await store.dispatch("profile/getUserFollowing", { slug, ownData });

        if (store.getters["auth/group"] !== "regular") {
          await store.dispatch("profile/getUserConnections", {
            slug,
            ownData
          });

          await store.dispatch("profile/getRequestedConnections");
          await store.dispatch("profile/getPendingConnections");
        }
      }
      next();
    }
  },
  {
    path: "/email",
    name: "EmailVerification",
    component: () => import("@/pages/EmailPage/EmailPage.vue"),
    beforeEnter: async (to, from, next) => {
      const { verify_email: token = "" } = to.query;

      if (token) {
        const { success } = await store.dispatch("auth/verifyEmail", { token });

        if (success) next();
        else next({ name: "404" });
      } else next({ name: "Home" });
    }
  },
  {
    path: "/404",
    name: "404",
    component: () => import("@/pages/LinkErrorPage/LinkErrorPage.vue")
  },
  {
    path: "*",
    redirect: { name: "Home" }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition;
    return { x: 0, y: 0 };
  }
});

export default router;
