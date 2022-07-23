function handleReplyButton(responseId) {
    const replyFormContainer = document.getElementById(`reply-form-container-${responseId}`);
    replyFormContainer.className = 'reply-form-container.enabled'  // taken help of css here, we're setting the class
  }
  
  function handleCancelReply(responseId) {
    const replyFormContainer = document.getElementById(`reply-form-container-${responseId}`);
    replyFormContainer.className = 'reply-form-container'
  }
// these functions just enables or disables tha reply container
