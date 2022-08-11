import { request } from "@/services";

export default {
  data() {
    return {
      topics: [
        "Anxiety Philippines",
        "COVID-19",
        "Mental Health Day",
        "Cabin Fever",
        "Dolomite for Mental Health"
      ],
      items: []
    };
  },
  async mounted() {
    const response = await request("top/tags/");

    console.log(response);

    this.items = [...response.data.items];

    console.log(response.data.items);
  }
};
