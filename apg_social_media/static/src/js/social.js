/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

// const custLikebtn = document.getElementById('custLikebtn');  // Copy button ID
// const custCommentbtn = document.getElementById('custCommentbtn');  // Copy button ID
// const custSharebtn = document.getElementById('custSharebtn');  // Copy button ID
// const icon = document.querySelector('#likeIcon');
// const commentInput = document.getElementById('comment-input-1');
// const postId = document.getElementById('post_id');

$(document).ready(function() {
    var currentUrl = window.location.pathname;
    if (currentUrl === '/forumsection') {
        $("header").hide();
        $("footer").hide();
    }
});

publicWidget.registry.custPost = publicWidget.Widget.extend({
    selector: '.o-cust-post',
    events: {
        'click #custLikebtn': '_like_post',
        'keydown #comment-input-1': '_comment_post',
        'click #custSharebtn': '_share_post',  // Added Share Button Click Event
        // 'click #custSharebtn': 'generate_otp',
    },


    // start: async function () {
    //     await this._fetch_like_status();  // Fetch like status when widget starts
    //     // return this._super(...arguments);
    //     return this._super.apply(this, arguments);
    // },

    // start: async function () {
    //     const res = await this._super(...arguments);
    //     await this._fetch_like_status();
    //     return res;
    // },

    /**
     * Fetch initial like status from the backend and update the UI
     */
    // _fetch_like_status: async function () {
    //     const post_id = postId.value;  // Ensure this field is in your template
    //     console.log(">>>>>>>>>>>post_id<<<<<<<<<<<",post_id)
    //     if (post_id) {
    //         try {
    //             const url = `/post/like_status`;
    //             const params = {
    //                 'post_id' : post_id,
    //             };
    //             const response = await rpc(url, params);
    //             console.log(">>>>>>>>>>>response<<<<<<<<<<<",response)
    //             if (response.liked) {
    //                 icon.classList.add('liked');  // Add 'liked' class if liked
    //             } else {
    //                 icon.classList.remove('liked');  // Remove 'liked' class if not liked
    //             }
    //         } catch (error) {
    //             console.error('Error fetching like status:', error);
    //         }
    //     }
    // },

    _share_post: function (event) {
        const currentUrl = window.location.href; // Get current URL
        navigator.clipboard.writeText(currentUrl).then(() => {
            alert("Link copied to clipboard!");
        }).catch(err => {
            console.error('Failed to copy:', err);
            alert("Failed to copy the link.");
        });
    },

    _like_post: async function (event) {
        // Toggle the 'liked' class to change the color
        // const post_id = postId.value;
        const button = event.currentTarget;  // Get the clicked button
        const post_id = button.getAttribute('data-post-id');  // Fetch the post ID
        const icon = button.querySelector('#likeIcon')
        if (icon.classList.contains('liked')) {
            try {
                const url = `/post/unlike`;
                const params = {
                    'post_id' : post_id,
                };
                const response = await rpc(url, params);
                if (response.success) {
                    icon.classList.remove('liked');
                } else {
                    alert('Error with Like.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to Like post.');
            }
            
        } else {
            try {
                const url = `/post/like`;
                const params = {
                    'post_id' : post_id,
                };
                const response = await rpc(url, params);
                if (response.success) {
                    icon.classList.add('liked');
                } else {
                    alert('Error with Like.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to Like post.');
            }
            
        } 
    },

    _comment_post: async function (event) {
        // const icon = button.querySelector('#likeIcon')
        if (event.key === 'Enter') {
            const commentInput = event.currentTarget;  // Get the input field
            const post_id = commentInput.getAttribute('data-comment-post-id');  // Fetch the post ID
            const commentText = commentInput.value.trim();  // Get the comment text
            if (commentText) {
                try {
                    const url = `/post/comment`;
                    const params = {
                        'comment' : commentText,
                        'post_id' : post_id,
                    };
                    const response = await rpc(url, params);
                    if (response.success) {

                        const commentList = document.getElementById(`comment-list-${post_id}`);  // Correct comment list
                        // const commentDiv = document.createElement('div');
                        // commentDiv.classList.add('comment-item');
                        // commentDiv.textContent = commentText;
                        // commentList.appendChild(commentDiv);
                        // commentInput.value = '';  // Clear the input field



                        // const commentList = document.getElementById('comment-list-1');
                        const mainDiv = document.createElement('div');
                        const userDetailDiv = document.createElement('div');
                        const commentDiv = document.createElement('div');
                        const dataDiv = document.createElement('div');
                        const nameSpan = document.createElement('span');
                        const dateSpan = document.createElement('span');
                        const userDataImg = document.createElement('img');
                        nameSpan.setAttribute('class', 'user-name');
                        nameSpan.textContent = "John Doe";
                        dateSpan.setAttribute('class', 'post-date');
                        dateSpan.textContent = "Dec 14, 2024, 10:00 AM";
                        userDataImg.classList.add('user-image', 'comment-user-icon');
                        // userDataImg.setAttribute('class', );
                        userDataImg.setAttribute('src', '/custom_web_kreator/static/src/user1.png');
                        mainDiv.classList.add('comment-header');
                        userDetailDiv.classList.add('user-details', 'comment-user');
                        dataDiv.classList.add('comment-details');
                        userDetailDiv.appendChild(nameSpan);
                        userDetailDiv.appendChild(dateSpan);
                        mainDiv.appendChild(userDataImg);
                        mainDiv.appendChild(userDetailDiv);
                        commentDiv.appendChild(dataDiv);
                        dataDiv.textContent = commentText;
                        commentList.appendChild(mainDiv);
                        commentList.appendChild(commentDiv);
                        commentInput.value = '';  // Clear input field
                    } else {
                        alert('Error submitting comment.');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Failed to submit comment.');
                }
            }
        }
    },
});
