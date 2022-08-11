import { AdsTrendsColumn, StickySideSection } from "@/views/components";

export default {
  components: {
    AdsTrendsColumn,
    StickySideSection
  },

  data() {
    return {
      gad7Options: [
        "Not at all",
        "Several days",
        "More than half the days",
        "Nearly every day"
      ],
      pssOptions: [
        "Never",
        "Almost never",
        "Sometimes",
        "Fairly often",
        "Very often"
      ],
      gad7Answers: [null, null, null, null, null, null, null],
      gad7Score: 0,
      gad7Questions: [
        "Feeling nervous, anxious, or on edge",
        "Not being able to stop or control worrying",
        "Worrying too much about different things",
        "Trouble relaxing",
        "Being so restless that it is hard to sit still",
        "Becoming easily annoyed or irritable",
        "Feeling afraid, as if something awful might happen "
      ],
      resultColor: {
        "Minimal Anxiety": "blue",
        "Mild Anxiety": "green",
        "Moderate Anxiety": "orange",
        "Severe Anxiety": "red"
      },
      pssQuestions: [
        "been upset because of something that happened unexpectedly",
        "felt that you were unable to control the important things in your life",
        "felt nervous and stressed",
        "felt confident about your ability to handle your personal problems",
        "felt that things were going your way",
        "found that you could not cope with all the things that you had to do",
        "been able to control irritations in your life",
        "felt that you were on top of things",
        "been angered because of things that happened that were outside of your control",
        "felt difficulties were piling up so high that you could not overcome them"
      ],
      pssAnswers: [null, null, null, null, null, null, null, null, null, null],
      pssScore: 0,
      pssResultColor: {
        "Low Stress": "blue",
        "Moderate Stress": "orange",
        "High Perceived Stress": "red"
      }
    };
  },
  computed: {
    gadResult() {
      let result = "";
      if (this.gad7Score >= 0 && this.gad7Score <= 4)
        result = "Minimal Anxiety";
      else if (this.gad7Score >= 5 && this.gad7Score <= 9)
        result = "Mild Anxiety";
      else if (this.gad7Score >= 10 && this.gad7Score <= 14)
        result = "Moderate Anxiety";
      else result = "Severe Anxiety";

      return result;
    },
    pssResult() {
      let result = "";

      if (this.pssScore >= 0 && this.pssScore <= 13) result = "Low Stress";
      else if (this.pssScore >= 14 && this.pssScore <= 26)
        result = "Moderate Stress";
      else result = "High Perceived Stress";

      return result;
    }
  },
  methods: {
    showGAD() {
      this.$refs.gad7Forms.showDialog();
    },
    showPSS() {
      this.$refs.pssForms.showDialog();
    },
    getGADResults() {
      const reducer = (accumulator, currentValue) => accumulator + currentValue;
      this.gad7Score = this.gad7Answers.reduce(reducer);

      this.$refs.gad7Forms.cancel();
      this.$nextTick(() => {
        this.$refs.gad7ResultsDialog.showDialog();
      });
    },
    onCloseGADDialog() {
      this.gad7Answers = this.gad7Answers.map(() => null);
    },
    onClosePSSDialog() {
      this.pssAnswers = this.pssAnswers.map(() => null);
    },
    getPSSResults() {
      const reducer = (accumulator, currentValue) => accumulator + currentValue;
      const reverseScoreItems = [4, 5, 7, 8];
      const modifiedScores = this.pssAnswers.map((answer, i) =>
        reverseScoreItems.includes(i + 1) ? 4 - answer : answer
      );

      this.pssScore = modifiedScores.reduce(reducer);

      this.$refs.pssForms.cancel();
      this.$nextTick(() => {
        this.$refs.pssResultsDialog.showDialog();
      });
    }
  }
};
