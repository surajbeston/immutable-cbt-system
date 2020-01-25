App = {
    loading: false,
    contracts: {},

    id : "",

    load: async() => {
        await App.loadWeb3();
        await App.loadAccount();
        await App.loadContract();
        await App.render()
    },

    loadWeb3: async () => {
        if (typeof web3 !== 'undefined') {
          App.web3Provider = web3.currentProvider
          web3 = new Web3(web3.currentProvider)
        } else {
          window.alert("Please connect to Metamask.")
        }
        // Modern dapp browsers...
        if (window.ethereum) {
          window.web3 = new Web3(ethereum)
          try {
            // Request account access if needed
            await ethereum.enable()
            // Acccounts now exposed
            web3.eth.sendTransaction({/* ... */})
          } catch (error) {
            // User denied account access...
          }
        }
        // Legacy dapp browsers...
        else if (window.web3) {
          App.web3Provider = web3.currentProvider
          window.web3 = new Web3(web3.currentProvider)
          // Acccounts always exposed
          web3.eth.sendTransaction({/* ... */})
        }
        // Non-dapp browsers...
        else {
          console.log('Non-Ethereum browser detected. You should consider trying MetaMask!')
        }
      },


      check_answers: () => {
        answers = ["ans11", "ans21", "ans32", "ans43", "ans54"]
        var radios = jQuery("input[type='radio']");
        score = 0
        var user_answers = radios.filter(":checked")
        console.log(user_answers)
        print (user_answers.length)
        if (user_answers.length == 5){
        for (var i = 0; i < 5; i++){
          if (answers[i] == user_answers[i].id){
            score += 10
            console.log(score)
          }
        }
        App.send_data(window.localStorage.getItem("user_id"), score, window.localStorage.getItem("name"))

      }
        else{
          console.log("There is error")
          $("#error").html("Please solve all questions.")
        }
      },


      give_access: (retrieved_data) => {
        console.log(retrieved_data)
        if (retrieved_data["detail"] == "ok"){
          if (retrieved_data["exam_ready"] == true){

              window.localStorage.setItem("name", retrieved_data["name"])
              window.location = "http://localhost:3000/home.html"

          }
          else{
            console.log("Invalid Exam Id.")
          }
        }
        else{
          console.log("Invalid Exam Id.")
        }
      },

      get_user: async (e) => {
        var user_id = document.getElementById("user_id").value
        console.log(user_id)
        data = new FormData()
        data.append('id', user_id)
        window.localStorage.setItem("user_id", user_id)

        fetch('http://localhost:8000/get/', {
        method: 'POST',
        body: data
        })
        .then(response => response.json())
        .then(jsonData =>  App.give_access(jsonData))
        .catch(err => {
                console.log(err)
            }
        )
      },

      load_user: () => {

        data = new FormData()
        user_id = window.localStorage.getItem("user_id")

        console.log(user_id)
        data.append('id', user_id)

        fetch('http://localhost:8000/get/', {
        method: 'POST',
        body: data
        })
        .then(response => response.json())
        .then(jsonData =>  {
          console.log(jsonData)
          $('#student_name').html(jsonData["name"])
          $('#student_id').html(jsonData["id"])
        })
        .catch(err => {
                console.log(err)
            }
        )
      },

      send_data: async (id, score, name) =>{

        //first send to server
        fetch('http://localhost:8000/submit-score/', {
        method: 'POST',
        body: data
        })
        .then(response => response.json())
        .then(jsonData =>  {
          console.log(jsonData)
          //then send to blockchain
          if (jsonData["detail"] != "exam already taken."){
            
          }
          
        })
        .catch(err => {
                console.log(err)
            }
        )
        await App.cbt.createTest(name, id, score)
        console.log("data saved in blockchain")
        data = new FormData()
        data.append('id', id)
        data.append('score', score)
        

        


      }
,     
    loadAccount: async () => {
        App.account = web3.eth.accounts[0]
    },

    loadContract: async () => {
        var cbt = await $.getJSON('cbt.json');

        App.contracts.cbt = TruffleContract(cbt);

        App.contracts.cbt.setProvider(App.web3Provider)

        App.cbt = await App.contracts.cbt.deployed()
    },

    render: async () => {
        var user_address = await App.account
        $('#address').html(user_address)
        
        data = new FormData()
        data.append('id', '0074dabb5da721fa4fc2bb0e28133eb3')

        fetch('http://localhost:8000/rank/', {
        method: 'POST',
        body: data
        })
        .then(response => response.json())
        .then(jsonData => console.log(jsonData))
        .catch(err => {
                console.log(err)
            }
        )
    },

    get_result_and_verify: () => {

      var user_id = document.getElementById("input_id").value
      console.log(user_id)
      var data = new FormData()

      data.append('id', user_id)
      data.append('kdj', 'sdfasdf')

      window.localStorage.setItem("user_id", user_id)

      fetch('http://localhost:8000/rank/', {
        method: 'POST',
        body: data
        })
        .then(response => response.json())
        .then(jsonData => {
            console.log(jsonData)
            document.getElementById("body").style.display = "block";
            document.getElementById("body").style.backgroundColor = "transparent";
            document.getElementById("body-form").style.display = "none";
            console.log("done")
            $("#name").html(jsonData["name"])
            $("#user_id").html(user_id)
            $("#score").html(jsonData["score"])
            window.localStorage.setItem("score", jsonData["score"])
            $("#rank").html(jsonData["rank"])
            $("#hash").html(jsonData["hash"])
            var a = jsonData["users"].length
          for (var i = 0; i < a; i++ ){
            console.log($(".particular"))
            const $holder = $(".particular").clone()
            console.log("I'm here")
            $holder.find(".name_other").html(jsonData["names"][i])
            $holder.find(".score_other").html(jsonData["users"][i]["score"])
            $holder.find(".hash_other").html(jsonData["users"][i]["hashed"])
            $("#other_results").append($holder)
          }
        })
        .catch(err => {
                console.log(err)
            }
        )

        console.log("sdfds")
    },

    check_authenticity: async () => {
      var count = await App.cbt.user_count()
      user_id = window.localStorage.getItem("user_id")
      score = window.localStorage.getItem("score")
      for (var i = 0; i < count.toNumber(); i++){

        var test = await App.cbt.tests()
        if (test.id == user_id){
          if (test.score.toNumber() == score){
            alert("Your data is safe!")
          }
          else{
            alert("Your data is altered!")
          }
        }
      }
    }
    
    }


$(() => {
    $(window).load(() => {
      App.load()
    })
  })