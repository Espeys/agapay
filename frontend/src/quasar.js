import Vue from "vue";

import "./styles/quasar.sass";
import "quasar/dist/quasar.ie.polyfills";
import "@quasar/extras/fontawesome-v5/fontawesome-v5.css";
import "@quasar/extras/eva-icons/eva-icons.css";

import { Quasar, LocalStorage, Notify } from "quasar";

Vue.use(Quasar, {
  config: {},
  plugins: { LocalStorage, Notify }
});
