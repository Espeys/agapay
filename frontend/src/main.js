import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import "typeface-source-sans-pro";
import "./quasar";

// helpers and services
import axios from "axios";
import ReactiveProvide from "vue-reactive-provide";
import linkify from "vue-linkify";
import vueNumeralFilterInstaller from "vue-numeral-filter";
import "@/plugins/Dayjs";

// components
import { AppFormInput, AppDialog } from "@/components";

Vue.config.productionTip = false;

axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;
axios.interceptors.response.use(
  response => {
    if (
      response.data.errors &&
      response.data.errors.some(error => error.code === 0)
    ) {
      // store.dispatch("forms/disableFormEditing");
      // router.replace({ name: "Error 500" });
    }

    return response;
  },
  error => {
    if (
      error.request.responseType === "blob" &&
      error.response.data instanceof Blob &&
      error.response.data.type &&
      error.response.data.type.toLowerCase().indexOf("json") != -1
    ) {
      return new Promise((resolve, reject) => {
        let reader = new FileReader();
        reader.onload = () => {
          error.response.data = JSON.parse(reader.result);
          resolve(Promise.reject(error));
        };

        reader.onerror = () => {
          reject(error);
        };

        reader.readAsText(error.response.data);
      });
    }

    switch (error.response.status) {
      case 401:
        // store.dispatch("forms/disableFormEditing");
        // store.dispatch("auth/destroyUserCredentials").then(() => {
        //   router.replace({ name: "Error 401" });
        // });
        store.dispatch("auth/destroyUserCredentials");
        // router.replace({ name: "Home" });
        break;
      case 403:
        // store.dispatch("forms/disableFormEditing");
        // router.replace({ name: "Error 403" });
        break;
      case 500:
      case 502:
        // store.dispatch("forms/disableFormEditing");
        // router.replace({ name: "Error 500" });
        break;
    }

    return Promise.reject(error);
  }
);

const getAuthToken = () => localStorage.getItem("accessToken");

axios.interceptors.request.use(function(config) {
  if (config.data instanceof FormData) {
    config.headers["Content-Type"] = "multipart/form-data";
  } else config.headers["Content-Type"] = "application/json";
  const token = getAuthToken();
  if (token) config.headers["Authorization"] = `Bearer ${token}`;
  return config;
}, undefined);

Vue.use(ReactiveProvide);
Vue.directive("linkified", linkify);
Vue.use(vueNumeralFilterInstaller);

Vue.component("app-form-input", AppFormInput);
Vue.component("app-dialog", AppDialog);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
