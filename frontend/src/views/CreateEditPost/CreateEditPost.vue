<template>
  <div class="row justify-lg-around q-pl-md-lg q-pl-lg-none">
    <div class="col-12 col-md-8 col-lg-7">
      <div class="q-pa-md q-pa-md-none q-mb-sm q-mb-md-lg">
        <span
          class="text-h4 text-weight-medium"
          v-text="sharedPostSlug ? 'Share Post' : 'Create Post'"
        ></span>
      </div>
      <div class="q-px-md q-px-md-none">
        <div class="q-mb-md">
          <app-form-input
            v-model="type"
            field-type="select"
            label="Post Type"
            class="text-weight-bold"
            :options="filteredPostTypes"
            :disabled="loading"
            outlined
            emit-value
            map-options
          >
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps" v-on="scope.itemEvents">
                <q-item-section avatar>
                  <q-icon :name="scope.opt.icon" class="q-ml-sm" size="22px" />
                </q-item-section>
                <q-item-section>
                  <q-item-label v-html="scope.opt.label" />
                  <q-item-label
                    caption
                    :class="$q.dark.isActive ? 'white' : 'text-grey-9'"
                    >{{ scope.opt.description }}</q-item-label
                  >
                </q-item-section>
              </q-item>
            </template>
          </app-form-input>
        </div>
      </div>

      <q-card
        class="q-pa-lg relative-position"
        :square="$q.screen.lt.md"
        bordered
      >
        <div v-if="type === 'diary'" class="q-mb-md">
          <app-form-input
            :value="$date().format('MMMM DD, YYYY')"
            outlined
            disabled
            prefix="Date:"
          ></app-form-input>
        </div>
        <div class="q-mb-md q-px-lg row justify-center">
          <vue-feedback-reaction
            v-if="type === 'diary'"
            class="q-mb-md"
            v-model="feedback"
            :labels="labels"
            :emoji-width="$q.screen.lt.md ? '40px' : '50px'"
            :emoji-height="$q.screen.lt.md ? '40px' : '50px'"
          />
        </div>
        <app-form-input
          v-model="postContent"
          :placeholder="
            type !== 'diary'
              ? 'What do you want to share with us? 😊'
              : 'How are you feeling today?'
          "
          outlined
          type="textarea"
          rows="6"
        ></app-form-input>
        <div class="q-mt-sm row items-center">
          <q-btn
            :class="{ 'on-left': !isRegularUser }"
            size="md"
            dense
            flat
            round
          >
            <q-icon
              name="far fa-grin"
              size="22px"
              :color="$q.dark.isActive ? 'white' : 'grey-9'"
            ></q-icon>
            <q-menu>
              <v-emoji-picker
                emoji-size="24"
                emojis-by-row="8"
                :dark="$q.dark.isActive"
                @select="postContent += $event.data"
              />
            </q-menu>
          </q-btn>
          <q-btn
            v-if="!isRegularUser"
            @click="fileUpload"
            dense
            flat
            round
            size="md"
          >
            <q-icon
              name="far fa-image"
              size="22px"
              :color="$q.dark.isActive ? 'white' : 'grey-9'"
            ></q-icon>
          </q-btn>
          <q-space></q-space>
          <app-form-input
            v-if="type !== 'diary'"
            v-model="isSensitiveContent"
            field-type="checkbox"
            label="Sensitive Content"
            class="text-body1"
          >
          </app-form-input>
        </div>
        <div v-if="uploadedPhoto" class="q-pt-sm q-pb-md">
          <q-img
            :src="uploadedPhotoURL"
            class="cursor-pointer rounded-borders relative-positon"
            style="width: 100%; height: 300px"
            @click.stop="showImage = !showImage"
          >
            <q-btn
              @click.stop="uploadedPhoto = null"
              class="absolute-right"
              color="negative"
            >
              <q-icon name="fas fa-trash" />
            </q-btn>
          </q-img>

          <FsLightbox :toggler="showImage" :sources="[uploadedPhotoURL]" />
        </div>
        <div class="q-my-md">
          <app-form-input
            v-if="type === 'promotion'"
            v-model="promotionType"
            field-type="select"
            label="Type of Promotion"
            class="text-weight-bold"
            :options="promotionOptions"
            outlined
            emit-value
            map-options
          />
          <app-form-input
            v-else-if="type === 'request' || type === 'offer'"
            v-model="helpType"
            field-type="select"
            :label="
              type === 'request'
                ? 'What kind of help are you requesting?'
                : 'What kind of help are you requesting?'
            "
            class="text-weight-bold"
            :options="helpOptions"
            outlined
            emit-value
            map-options
          />
        </div>
        <div class="q-mt-sm">
          <app-form-input
            v-if="type !== 'diary' && !sharedPostSlug"
            v-model="tags"
            field-type="select"
            @new-value="createValue"
            hint="Press Enter to add tag"
            input-debounce="0"
            use-input
            use-chips
            multiple
            hide-dropdown-icon
            outlined
            clearable
          >
            <template #selected>
              <span>Tags: </span>
              <template v-if="tags">
                <q-chip
                  v-for="(tag, i) in tags"
                  :key="tag"
                  dense
                  square
                  color="accent"
                  text-color="white"
                  class="text-weight-medium"
                  removable
                  icon-remove="fas fa-times"
                  @remove="$delete(tags, i)"
                >
                  <span v-text="tag" />
                </q-chip>
              </template>
            </template>
          </app-form-input>
        </div>
        <div v-if="sharedPostSlug" class="q-mt-md">
          <base-post :post="sharedPost" shared></base-post>
        </div>
        <div class="q-mt-md row">
          <q-space></q-space>
          <q-btn
            @click="createPost"
            :disable="!postContent && !uploadedPhoto && !sharedPostSlug"
            color="primary"
            no-caps
          >
            <span v-text="sharedPostSlug ? 'Share' : 'Post'" />
          </q-btn>
        </div>
        <input
          @change="onUpload"
          type="file"
          ref="fileUploader"
          v-show="false"
          accept=".png,.jpeg,.jpg"
        />
        <q-inner-loading :showing="loading">
          <q-spinner-hourglass color="primary" size="5.5em" class="q-mb-md" />
          <span class="text-body2"> Please wait ...</span>
        </q-inner-loading>
      </q-card>
    </div>
    <div class="col-12 col-md-2 col-lg-4 gt-md">
      <ads-trends-column></ads-trends-column>
      <sticky-side-section></sticky-side-section>
    </div>
  </div>
</template>

<script src="./CreateEditPost.js" />
