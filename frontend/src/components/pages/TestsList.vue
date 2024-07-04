<template>
  <Menu/>
  <Toast/>

  <Container>
    <div class="mx-2 m-5">
      <div class="search-panel flex">
        <div class="p-fluid m-2 search-input">
          <div class="p-input-icon-left p-float-label">
            <i class="pi pi-search"/>
            <InputText v-model="search" class="w-full"/>
            <label>Поиск теста</label>
          </div>
        </div>
        <div class="p-fluid m-2 search-input">
          <div class="p-float-label">
            <Chips v-model="selectedTags" class="w-full"/>
            <label>Укажите теги</label>
          </div>
        </div>
      </div>
    </div>

    <div v-if="openTests!==null" class="flex flex-wrap px-3 justify-content-center gap-3">
      <div v-for="test in filteredTests">
        <TestCard @tagClick="tag => selectedTags.push(tag)" :test="test" :open-test-times="getTestOpenTime(test)"/>
      </div>
    </div>
  </Container>

  <Footer/>
  <ScrollTop/>

</template>

<script lang="ts">
import Button from "primevue/button";
import Chips from "primevue/chips";
import Checkbox from "primevue/checkbox";
import InputText from "primevue/inputtext";
import ScrollTop from "primevue/scrolltop";
import Toast from 'primevue/toast';

import Menu from "@/components/Menu.vue";
import Container from "@/components/Container.vue";
import api from "@/services/api.js";
import Footer from "@/components/Footer.vue";
import TestCard from "@/components/TestCard.vue";
import {createNewTestAboutList, TestAbout} from "@/questions";
import {HandleError} from "@/helper";
import {UserOpenedQuestionTimes} from "@/userOpenedQuestions";

export default {
  name: "TestsList",
  components: {
    Footer,
    Button,
    Chips,
    Checkbox,
    Container,
    InputText,
    Menu,
    ScrollTop,
    TestCard,
    Toast,
  },

  data() {
    return {
      allTests: null as Array<TestAbout>,
      search: "",
      selectedTags: [] as Array<string>,
      openTests: null as any,
    }
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
    filteredTests(): TestAbout[] {
      if (!this.allTests) return [];
      return this.allTests.filter(
          (test: TestAbout) => {
            return this.filterByTestName(test) && this.filterByTags(test)
          }
      )
    }
  },

  mounted() {
    api.get("open_questions/").then(
        res => {
          this.openTests = res.data
        },
        error => HandleError(this, error)
    )
    api.get("questions/groups").then(
        res => {
          this.allTests = createNewTestAboutList(res.data)
        },
        error => HandleError(this, error)
    )
  },

  methods: {
    getTestOpenTime(test: TestAbout): UserOpenedQuestionTimes | undefined {
      if (!this.openTests) return undefined;
      return <UserOpenedQuestionTimes | undefined>this.openTests[test._id]
    },
    filterByTestName(test: TestAbout): boolean {
      return this.search.length === 0 || test.name.includes(this.search)
    },
    filterByTags(test: TestAbout): boolean {
      return this.selectedTags.length === 0 || this.selectedTags.every((tag: string) => {
        return test.tags.indexOf(tag) >= 0
      })
    },
  }
}
</script>

<style scoped>

.search-panel {
  display: flex;
}

.search-input {
  width: 50%
}

@media (width < 760px) {
  .search-panel {
    flex-wrap: wrap;
  }

  .search-input {
    width: 100%
  }
}

</style>