<script>
  import Button from "../shared/Button.svelte";
  let fileInput;

  function handleFiles(event) {
    const files = event.target.files;
    // Further file handling logic can go here
  }

  function triggerFileSelect(event) {
    event.preventDefault();
    fileInput.click(); 
  }
</script>

<main>
  <div id="drop-area">
    <form class="my-form">
      <label for="fileElem" class="file-label">Drag the file</label>
      <div class="buttons">
        <div class="new-button">
          <input 
            type="file" 
            id="fileElem" 
            multiple 
            accept="image/*" 
            bind:this={fileInput} 
            on:change={handleFiles} 
            style="display: none;" 
          />
          <Button inverse={true} on:click={triggerFileSelect}>
            Choose File
          </Button>
        </div>
      </div>
    </form>
  </div>
</main>

<style>
  #drop-area {
    border: 2px dashed #949494;
    border-radius: 20px;
    width: 270px;
    height: 280px;
    font-family: sans-serif;
    margin: 5px auto;
    padding: 20px;
    background: #fbede9;
    float: left;
    text-align: center;
    box-shadow: 6px 6px 10px #949494;
    scale: 1.4;
  }
  #fileElem {
    display: none;
  }
  .file-label {
    cursor: pointer;
    color: #333;
    font-weight: bold;
  }
  .my-form {
    margin-bottom: 10px;
    margin-top: 75px;
    align-items: center;
  }
  .buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
  }
  .new-button {
    transform: scale(0.8);
    display: inline-block;
    color: black;
  }
</style>
