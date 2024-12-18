<template>
  <!-- Mode selection -->
  <div>
    View mode:
    <select v-model="mode">
      <option>Same prompt, different systems</option>
      <option>Same prompt, same system, different seeds</option>
    </select>
  </div>

  <!-- Prompt id selection -->
  <div>
    Prompt id (0 - {{ metadata.length - 1 }}):
    <input v-model="prompt_id"/>
    <button @click="randomize_prmompt_id">Random</button>
  </div>

  <br>

  <!-- Prompt -->
  <div>
    <p>Prompt:</p> 
    {{ metadata[prompt_id].prompt }}
  </div>

  <br>

  <!-- Mode-specific stuff -->
  <div v-if="mode === 'Same prompt, different systems'">
    <div v-for="system in Object.keys(metadata[prompt_id]).toSorted()" :key="system">
      <div v-if="(system !== 'prompt') && (system !== 'musiccaps_prompt_id')">
        <p>{{ system }}</p>
        <audio controls :key="prompt_id" preload="none">
          <source :key="prompt_id" :src="'https://humanratings-6207bc1e725a.herokuapp.com/'+metadata[prompt_id][system][0]" type="audio/wav">
          Your browser does not support the audio element.
        </audio>
      </div>
    </div>
  </div>

  <div v-else-if="mode === 'Same prompt, same system, different seeds'">
    System: 
    <select v-model="system">
      <option v-for="system in get_systems()" :key="system">
        {{ system }}
      </option>
    </select>
    <div v-for="url in metadata[prompt_id][system]" :key="url">
      <audio controls :key="url" preload="none">
        <source :key="url" :src="'https://humanratings-6207bc1e725a.herokuapp.com/'+url" type="audio/wav">
        Your browser does not support the audio element.
      </audio>
    </div>
  </div>
</template>

<script>
// Read the metadata json
import metadata from './assets/demo_metadata.json'

export default {
  data() {
    return {
      // Constants
      metadata: metadata,

      // Variables
      mode: 'Same prompt, different systems',
      prompt_id: '0',
      system: 'riffusion_inst'
    };
  },
  methods: {
    randomize_prmompt_id() {
      this.prompt_id = Math.floor(Math.random() * this.metadata.length).toString()
    },
    get_systems() {
      var systems = Object.keys(this.metadata[this.prompt_id]).toSorted()
      for (var i = 0; i < systems.length; i++) {
        if ((systems[i] === 'prompt') || (systems[i] === 'musiccaps_prompt_id')) {
          systems.splice(i, 1)
        }
      }
      return systems
    }
  }

};
</script>
