<template>
  <Menu/>
  <Toast/>

  <Container>
    <div class="mx-2 m-5 search-panel">
      <div class="p-input-icon-left p-float-label m-2 search-input">
        <i class="pi pi-search" />
        <InputText v-model="search" style="width: 100%"/>
        <label>Поиск теста</label>
      </div>
      <div class="card p-fluid m-2 search-input">
        <div class="p-float-label">
          <Chips v-model="selectedTags" style="width: 100%"/>
          <label>Укажите теги</label>
        </div>
      </div>
    </div>
  </Container>

    <div class="flex flex-wrap px-3 justify-content-center">
      <div v-for="test in filteredTests">
        <TestCard @tagClick="tag => selectedTags.push(tag)" :test="test"/>
      </div>
    </div>

  <Footer/>
  <ScrollTop/>

</template>

<script lang="ts">
import Button from "primevue/button";
import Chips from "primevue/chips";
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

export default {
  name: "TestsList",
  components: {
    Footer,
    Button,
    Chips,
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
    }
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
    filteredTests() {
      if (!this.allTests) return [];
      return this.allTests.filter(
          (test: TestAbout) => {
            return this.filterByTestName(test) && this.filterByTags(test)
          }
      )
    }
  },

  mounted() {
    api.get("questions/groups").then(
        res => {
          this.allTests = createNewTestAboutList(res.data)
        },
        error => HandleError(this, error)
    )
  },

  methods: {
    filterByTestName(test: TestAbout): boolean {
      return this.search.length === 0 || test.name.includes(this.search)
    },
    filterByTags(test: TestAbout): boolean {
      return this.selectedTags.length === 0 || this.selectedTags.every((tag: string) => {return test.tags.indexOf(tag) >= 0})
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