<script>
  import Button from "../shared/Button.svelte"; 
  function handleFiles(files){
    console.log("Files selected :", files);
  }
</script>

<main>
  <div id="drop-area">
    <form class="my-form">
      <label for= "fileElem" class = "file-label">Drag the file</label>
      <div class="buttons">
        <div class="new-button">
          <input 
          type = "file" 
          id ="fileElem" 
          multiple 
          accept ="image/*" 
          style = "display: none;"
          />
        <Button inverse={true} on:click={(e) => 
        { e.preventDefault(); 
        document.getElementById('fileElem').click();
        }} > 
        Choose File 
      </Button>
        </div>
      </div>
    </form>
  </div>
</main>  

<style>
  #drop-area {
  border: 2px dashed #ccc;
  border-radius: 20px;
  width: 240px;
  height: 240px;
  font-family: sans-serif;
  margin: 5px auto;
  padding: 20px;
  background: #fbede9;
  float: left;
  text-align : center;
}
#drop-area.highlight {
  border-color: #fbede9;
}
p {
  margin-top: 0;
}
#fileElem {
  display: none;
}
.file-label {
  cursor : pointer;
  color : #333;
  font-weight: bold;
}
.my-form {
  margin-bottom: 10px;
  margin-top: 75px;
  align-items: center;
}

#gallery {
  margin-top: 10px;
}
#gallery img {
  width: 150px;
  margin-bottom: 10px;
  margin-right: 10px;
  vertical-align: middle;
  background: #fbede9;
}

.button:hover {
  background: #fbede9;
}


.buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 15px;
  
}
.new-button {
  transform: scale(0.6); /* Scale down to 80% */
  display: inline-block;
  color: black

}

</style>
