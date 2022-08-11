<template>
  <div class="row justify-lg-around q-pl-md-lg q-pl-lg-none">
    <div class="col-12 col-md-8 col-lg-7">
      <div class="q-pa-md q-pa-md-none">
        <span class="text-h4 text-weight-medium"
          >Psychological Self-Assessment Test</span
        >
        <div
          class="q-mt-sm"
          :class="$q.screen.gt.sm ? 'row no-wrap ' : 'column items-center'"
        >
          <p class="text-body1 q-mb-none q-mt-sm">
            Get an initial screening of your mental health condition by trying
            these psychological self-assessment test with a real-time result
          </p>
          <div>
            <q-img :src="require('@/assets/test.svg')" width="320px"></q-img>
          </div>
        </div>
      </div>
      <q-card bordered class="q-px-md q-py-lg">
        <q-list>
          <q-item class="q-mb-md">
            <q-item-section avatar top>
              <q-avatar size="100px" class="q-mr-md">
                <q-img
                  src="https://image.freepik.com/free-vector/fear-missing-out-concept-with-man_23-2148656620.jpg"
                ></q-img>
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label>
                <span class="text-h6 text-weight-bold">
                  GAD-7 (General Anxiety Disorder-7)</span
                >
              </q-item-label>
              <q-item-label class="text-body1">
                The Generalized Anxiety Disorder scale (GAD-7) is one of the
                most frequently used diagnostic self-report scales for
                screening, diagnosis and severity assessment of anxiety
                disorder.
              </q-item-label>
              <q-item-label
                class="text-body1 q-mt-sm row items-center no-wrap"
                v-linkified:options="{ className: 'post-content-link' }"
                lines="1"
              >
                <q-icon name="fas fa-link" left />
                https://adaa.org/sites/default/files/GAD-7_Anxiety-updated_0.pdf
              </q-item-label>
              <div class="q-mt-md">
                <q-btn
                  @click="showGAD"
                  :class="{ 'full-width q-mt-sm': $q.screen.lt.md }"
                  color="primary"
                  no-caps
                  rounded
                  >Take the test</q-btn
                >
              </div>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section avatar top>
              <q-avatar size="100px" class="q-mr-md">
                <q-img
                  src="https://img.freepik.com/free-vector/fear-missing-out-concept_23-2148662908.jpg?size=338&ext=jpg"
                ></q-img>
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label>
                <span class="text-h6 text-weight-bold">
                  PSS (Perceived Stress Scale)</span
                >
              </q-item-label>
              <q-item-label class="text-body1">
                The Perceived Stress Scale (PSS) is the most widely used
                psychological instrument for measuring the perception of stress.
                It is a measure of the degree to which situations in one's life
                are appraised as stressful. Items were designed to tap how
                unpredictable, uncontrollable, and overloaded respondents find
                their lives.
              </q-item-label>
              <q-item-label
                class="text-body1 q-mt-sm row items-center no-wrap"
                v-linkified:options="{ className: 'post-content-link' }"
                lines="1"
              >
                <q-icon name="fas fa-link" left />
                https://das.nh.gov/wellness/docs/percieved%20stress%20scale.pdf
              </q-item-label>
              <div class="q-mt-md">
                <q-btn
                  @click="showPSS"
                  :class="{ 'full-width q-mt-sm': $q.screen.lt.md }"
                  color="primary"
                  no-caps
                  rounded
                  >Take the test</q-btn
                >
              </div>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card>
      <div>
        <p class="text-caption q-mt-md">
          <span class="text-weight-medium">
            Disclaimer: The scores on the following self-assessment do not
            reflect any particular diagnosis or course of treatment.
          </span>
          They are meant as a tool to help assess your level of stress or
          anxiety. If you have any further concerns about your current
          well-being, you may have a consultation with legitimate mental health
          professionals (visit
          <router-link :to="{ name: 'Service Providers' }"
            ><span class="link-text text-primary text-weight-bold"
              >Service Providers</span
            ></router-link
          >).
        </p>
      </div>
    </div>
    <div class="col-12 col-md-2 col-lg-4 gt-md">
      <ads-trends-column></ads-trends-column>
      <sticky-side-section></sticky-side-section>
    </div>
    <app-dialog
      ref="gad7Forms"
      :maximized="$q.screen.lt.md"
      width="720px"
      card-class="q-pa-lg"
      @close-dialog="onCloseGADDialog"
      close
    >
      <template #header>
        <span> GAD-7 (General Anxiety Disorder-7)</span>
      </template>

      <div class="q-px-md">
        <div
          v-for="(question, i) in gad7Questions"
          :key="question"
          class="q-mb-lg"
        >
          <div class="row items-center no-wrap">
            <q-avatar
              color="accent"
              text-color="white"
              size="md"
              class="q-mr-md"
            >
              <span v-text="i + 1" class=" text-h6 text-weight-bold" />
            </q-avatar>

            <span
              v-text="
                `Over the last two weeks, how often have you been bothered by ${question.toLowerCase()}?`
              "
              class="text-h6"
            />
          </div>
          <div class="column q-mt-sm text-body1" style="margin-left: 36px">
            <q-radio
              v-for="(option, value) in gad7Options"
              :key="option"
              v-model="gad7Answers[i]"
              :val="value"
              :label="option"
            />
          </div>

          <q-separator
            v-if="i < gad7Questions.length - 1"
            class="q-my-md"
          ></q-separator>
        </div>
        <q-btn
          @click="getGADResults"
          :disabled="gad7Answers.some(answer => typeof answer !== 'number')"
          class="full-width q-mt-sm"
          color="primary"
          no-caps
        >
          Analyze my answers
        </q-btn>
      </div>
    </app-dialog>
    <app-dialog
      ref="gad7ResultsDialog"
      :maximized="$q.screen.lt.md"
      width="560px"
      card-class="q-pa-lg"
      @close-dialog="gad7Score = 0"
      close
    >
      <template #header>
        <span> GAD-7 (General Anxiety Disorder-7)</span>
      </template>

      <div class="text-center">
        <span class="text-weight-regular text-h6"
          >The result of your test is</span
        >
        <div :class="`text-${resultColor[gadResult]}`">
          <span class="text-h3 text-weight-bold" v-text="gad7Score" />

          <p class="text-body1 text-weight-medium" v-text="gadResult" />
        </div>

        <p class="text-body2">
          <span class="text-weight-medium">
            The scores on the following self-assessment do not reflect any
            particular diagnosis or course of treatment.
          </span>
          They are meant as a tool to help assess your level of stress or
          anxiety.
        </p>
        <q-separator class="q-mb-md"></q-separator>
        <span class="text-body1"
          >In case you want to know how to handle this situation, please go to
          <router-link :to="{ name: 'Emotional Mental Health' }"
            ><span class="link-text text-primary text-weight-bold"
              >Emotional and Mental Health</span
            ></router-link
          >
          page for additional information.</span
        >
      </div>
    </app-dialog>

    <app-dialog
      ref="pssForms"
      :maximized="$q.screen.lt.md"
      width="720px"
      card-class="q-pa-lg"
      @close-dialog="onClosePSSDialog"
      close
    >
      <template #header>
        <span> PSS (Perceived Stress Scale)</span>
      </template>

      <div class="q-px-md">
        <div
          v-for="(question, i) in pssQuestions"
          :key="question"
          class="q-mb-lg"
        >
          <div class="row items-center no-wrap">
            <q-avatar
              color="accent"
              text-color="white"
              size="md"
              class="q-mr-md"
            >
              <span v-text="i + 1" class=" text-h6 text-weight-bold" />
            </q-avatar>

            <span
              v-text="
                `In the last month, how often have you ${question.toLowerCase()}?`
              "
              class="text-h6"
            />
          </div>
          <div class="column q-mt-xs q-ml-lg text-body1">
            <q-radio
              v-for="(option, value) in pssOptions"
              :key="option"
              v-model="pssAnswers[i]"
              :val="value"
              :label="option"
            />
          </div>

          <q-separator
            v-if="i < pssQuestions.length - 1"
            class="q-my-md"
          ></q-separator>
        </div>
        <q-btn
          @click="getPSSResults"
          :disabled="pssAnswers.some(answer => typeof answer !== 'number')"
          class="full-width q-mt-sm"
          color="primary"
          no-caps
        >
          Analyze my answers
        </q-btn>
      </div>
    </app-dialog>
    <app-dialog
      ref="pssResultsDialog"
      :maximized="$q.screen.lt.md"
      width="560px"
      card-class="q-pa-lg"
      @close-dialog="pssScore = 0"
      close
    >
      <template #header>
        <span> PSS (Perceived Stress Scale)</span>
      </template>

      <div class="text-center">
        <span class="text-weight-regular text-h6"
          >The result of your test is</span
        >
        <div :class="`text-${pssResultColor[pssResult]}`">
          <span class="text-h3 text-weight-bold" v-text="pssScore" />

          <p class="text-body1 text-weight-medium" v-text="pssResult" />
        </div>

        <p class="text-body2">
          <span class="text-weight-medium">
            The scores on the following self-assessment do not reflect any
            particular diagnosis or course of treatment.
          </span>
          They are meant as a tool to help assess your level of stress or
          anxiety.
        </p>
        <q-separator class="q-mb-md"></q-separator>
        <span class="text-body1"
          >In case you want to know how to handle this situation, please go to
          <router-link :to="{ name: 'Emotional Mental Health' }"
            ><span class="link-text text-primary text-weight-bold"
              >Emotional and Mental Health</span
            ></router-link
          >
          page for additional information.</span
        >
      </div>
    </app-dialog>
  </div>
</template>

<script src="./SelfAssessmentTest.js" />
