var inboxMessageContent = document.getElementsByClassName("inbox_message_content")[0];
var inboxMessage = document.getElementsByClassName("inbox_message_msg");
var messageTitle = document.getElementsByClassName("inbox_message_msg_content");
var inboxReceivedMessage = document.getElementsByClassName("inbox_received_message")[0];
var inboxMessageElement = document.getElementsByClassName("inbox_message");
var inboxReceivedMessageSenderAvatar = document.getElementsByClassName("inbox_received_message_sender_avatar_img")[0];
var inboxReceivedMessageSenderEmail = document.getElementsByClassName("inbox_received_message_sender_email")[0];
var inboxReceivedMessageReceiverAvatar = document.getElementsByClassName("inbox_received_message_receiver_avatar_img")[0];
var inboxReceivedMessageReceiverEmail = document.getElementsByClassName("inbox_received_message_receiver_email")[0];
var messageContentSender = document.getElementsByClassName("inbox_received_message_content_header_sender")[0];
var messageContentDatetime = document.getElementsByClassName("inbox_received_message_content_header_datetime")[0];
var messageContent = document.getElementsByClassName("inbox_received_message_content_content")[0];
var replyMessageLink = document.getElementsByClassName("reply_message_link")[0];
var senderEmail = document.getElementsByClassName("inbox_received_message_sender_email")[0];
var receiverEmail = document.getElementsByClassName("inbox_received_message_receiver_email")[0];

for (let i = 0; i < inboxMessage.length; i++) {

    inboxMessage[i].addEventListener("click", event => {

        inboxMessageContent.style.display = "none";
        inboxReceivedMessage.style.display = "block";
        inboxMessageElement[i].style.backgroundColor = "#657ee4";
        inboxReceivedMessageReceiverAvatar.setAttribute("src", `../static/uploads/images/${avatar}`);
        if (inboxMessages[i].avatar != false) inboxReceivedMessageSenderAvatar.setAttribute("src", `../static/uploads/images/${inboxMessages[i].avatar}`);
        else inboxReceivedMessageSenderAvatar.setAttribute("src", "../static/uploads/images/login-icon.jpg");
        messageContentSender.innerText = "From:  " + inboxMessages[i].author;
        messageContentSender.style.fontWeight = "bold";
        messageContentSender.style.paddingLeft = "14px";
        messageContentDatetime.innerText = inboxMessages[i].datetime;
        messageContent.innerText = inboxMessages[i].content;
        replyMessageLink.href = `/compose_message?recipient=${inboxMessages[i].author}`;
        senderEmail.innerText = allEmails[inboxMessages[i].author];
        receiverEmail.innerText = allEmails[inboxMessages[i].recipient];

    for (let j = 0; j < inboxMessage.length; j++) {

        if (i != j) {

            inboxMessageElement[j].style.backgroundColor = "#fff";

        }

    }

    })

}

console.log(inboxMessages.length);
