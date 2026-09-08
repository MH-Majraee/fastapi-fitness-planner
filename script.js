async function fetchWorkout(weekNum) {
    const userProfile = {
        age: parseInt(document.getElementById('age').value) || 0,
        gender: document.getElementById('gender').value,
        weight: parseFloat(document.getElementById('weight').value) || 0,
        height: parseFloat(document.getElementById('height').value) || 0,
        neck: parseFloat(document.getElementById('neck').value) || 0,
        chest: parseFloat(document.getElementById('chest').value) || 0,
        arm: parseFloat(document.getElementById('arm').value) || 0,
        waist: parseFloat(document.getElementById('waist').value) || 0,
        hip: parseFloat(document.getElementById('hip').value) || 0,
        thigh: parseFloat(document.getElementById('thigh').value) || 0,
        goal: document.getElementById('goal').value,
        days_per_week: parseInt(document.getElementById('days_per_week').value) || 3,
        experience: document.getElementById('experience').value,
        equipment: document.getElementById('equipment').value,
        duration: parseInt(document.getElementById('duration').value) || 60,
        activity_level: document.getElementById('activity_level').value,
        injuries: document.getElementById('injuries').value,
        week_number: weekNum
    };

    if (!userProfile.age || !userProfile.weight || !userProfile.height) {
        alert("لطفاً ابتدا فیلدهای اصلی فرم (سن، وزن، قد و ...) را پر کنید.");
        return;
    }

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `در حال بارگذاری برنامه هفته ${weekNum} توسط هوش مصنوعی...`;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/workout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userProfile)
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            resultDiv.innerHTML = `<h3>برنامه تمرینی هفته ${weekNum}</h3>` + marked.parse(data.workout_plan);
        } else {
            resultDiv.innerHTML = `خطا: ${data.workout_plan}`;
        }
    } catch (error) {
        console.error("خطا در ارتباط با سرور:", error);
        resultDiv.innerHTML = "خطا در ارتباط با سرور پایتون. مطمئن شوید سرور (Uvicorn) روشن است.";
    }
}

document.getElementById('workoutForm').addEventListener('submit', function(e) {
    e.preventDefault();
    fetchWorkout(1);
});