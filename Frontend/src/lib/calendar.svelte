<script>
    import { onMount } from "svelte";
    
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    
    let currentDate = new Date();
    let today = currentDate.getDate();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();
    
    let days = [];
    
    function generateCalendar(year, month) {
      days = [];
      let firstDay = new Date(year, month, 1).getDay();
      let lastDate = new Date(year, month + 1, 0).getDate();
    
      for (let i = 0; i < firstDay; i++) {
      days.push(null);
      }
    
      for (let i = 1; i <= lastDate; i++) {
      days.push(i);
      }
    }
    
    onMount(() => {
      generateCalendar(currentYear, currentMonth);
    });
    
    function goToPreviousMonth() {
      currentMonth--;
      if (currentMonth < 0) {
      currentMonth = 11;
      currentYear--;
      }
      generateCalendar(currentYear, currentMonth);
    }
    
    function goToNextMonth() {
      currentMonth++;
      if (currentMonth > 11) {
      currentMonth = 0;
      currentYear++;
      }
      generateCalendar(currentYear, currentMonth);
    }
</script>

    
<div class="navigation">
		<button on:click={goToPreviousMonth}>Previous</button>
		<div style="color: white;">{monthNames[currentMonth]} {currentYear}</div>
		<button on:click={goToNextMonth}>Next</button>
</div>

<div class="calendar">
		{#each dayNames as dayName}
		<div class="header">{dayName}</div>
		{/each}
		{#each days as day}
		<div class="day {day === today && currentMonth === currentDate.getMonth() && currentYear === currentDate.getFullYear() ? 'today' : ''} {day === null ? 'empty' : ''}">
			{day}
		</div>
		{/each}
</div>
  
  
<style>
	.calendar {
	  display: grid;
	  grid-template-columns: repeat(7, 1fr);
	  gap: 10px;
	  padding: 20px;
	  margin: auto;
	  background: #c4c4c4;
	  border-radius: 10px;
	  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	}
	.day {
	  width: auto;
	  height: auto;
	  display: flex;
	  justify-content: center;
	  align-items: center;
	  border-radius: 50%;
	  font-size: 14px;
	  color: #333;
	}
	.today {
	  background: #ff6347;
	  color: white;
	}
	.empty {
	  visibility: hidden;
	}
	.header {
	  font-weight: bold;
	  text-align: center;
	  color: green;
	}
	.navigation {
	  display: flex;
	  justify-content: space-between;
	  align-items: center;
	  margin-bottom: 10px;
	}
	button {
	  padding: 10px;
	  border: none;
	  background: #ff6347;
	  color: white;
	  border-radius: 5px;
	  cursor: pointer;
	}
	
</style>
