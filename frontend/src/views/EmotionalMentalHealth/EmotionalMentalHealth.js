import { AdsTrendsColumn, StickySideSection } from "@/views/components";
import { ManagingStressArticle } from "./components";
export default {
  components: {
    AdsTrendsColumn,
    StickySideSection,
    ManagingStressArticle
  },
  methods: {
    onClick(prevue) {
      console.log("click", prevue);
    }
  }
};
