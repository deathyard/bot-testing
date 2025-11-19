// Discord Bot JavaScript file
const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', () => {
    console.log('Bot is ready');
});

client.on('message', message => {
    if (message.content === '!flag') {
        // CTF flag hidden in devtools
        const flag = 'flag{check_devtools_file}';
        message.channel.send(flag);
    }
});

client.login('NjU2OTI3MDU0MTI1ODU4ODM2.Xfp0og.nYWB_S5pQhswE9Xg0VVChhMtCZk');
