import kue from 'kue';

const queue = kue.createQueue();

let jobData = {
    phoneNumber: '66668780',
    message: 'This is just a test message'
};

let job = queue.create('push_notification_code', jobData).save((err) => {
    if (!err) console.log(`Notification job created: ${job.id}`);
});

job.on('complete', () => {  
    console.log('Notification job completed');
});

job.on('failed', () => {    
    console.log('Notification job failed');
});

