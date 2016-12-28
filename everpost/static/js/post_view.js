$(function () {
    var comments = {};

    init();
    loadComments();

    function init() {
        if (currentUserId) {
            var panel = $('#new-comment-panel');
            panel.removeClass('invisible');
            $(panel).find('.parent-comment-reference').toggleClass('invisible');
            $('#new-comment-form').submit(addNewComment);
            $('#clear-reply-button').click(clearRecipient);
        }

        $('.load-more').click(loadComments);
    }

    function loadComments() {
        $.get(Urls.MORE_COMMENTS, function (data) {
            for (var i = 0; i < data.results.length; i++) {
                var item = data.results[i];
                addCommentItem(item);
            }

            if (Object.keys(comments).length == 0) {
                $('#no-comments-placeholder').removeClass('invisible');
            }

            $('.loader').addClass('invisible');
            if (data.next == null) {
                $('.load-more').addClass('invisible')
            } else {
                $('.load-more').removeClass('invisible')
            }
            Urls.MORE_COMMENTS = data.next;
        });
    }

    function highlightCommentOnClick(e) {
        var commentRef = $(e.target).attr('href');
        highlightComment(commentRef);
    }

    function highlightComment(commentRef) {
        $(commentRef).effect("highlight", {color: '#ffc060'}, 1000);
    }

    function addCommentItem(item) {
        var comment = new CommentModel(item);
        if (comments[comment.id]) {
            delete comments[comment.id];
            $('#comment-' + comment.id).remove();
        }
        comments[comment.id] = comment;

        var template = fillCommentTemplate(comment);
        template.appendTo("#comments-panel");
        template.show();
    }

    function fillCommentTemplate(comment) {
        var template = $("#comment-template").clone();
        template.attr("id", "comment-" + comment.id);

        if (comment.author.id) {
            var authorLink = $(template).find('.author-link');
            authorLink.text(comment.author.username);
            authorLink.attr('href', Urls.USER_POSTS.replace(Urls.PK_MASK, comment.author.id));

            $(template).find('.comment-time').text(comment.getCreatedAtString());

            if (currentUserId == comment.author.id) {
                var deleteCommentButton = $(template).find('.delete-comment-button');
                deleteCommentButton.click(deleteComment);
                deleteCommentButton.removeClass('invisible');
            }

            if (currentUserId) {
                var replyButton = $(template).find('.reply-button');
                replyButton.click(reply);
                replyButton.removeClass('invisible')
            }
        } else {
            $(template).find('.author-reference').addClass('invisible');
        }

        var parentCommentLink = $(template).find('.parent-comment-link');
        if (comment.parentCommentId != null) {
            parentCommentLink.text(comment.author.username);
            parentCommentLink.attr('href', '#comment-' + comment.parentCommentId);
            parentCommentLink.click(highlightCommentOnClick);
        } else {
            $(template).find('.parent-comment-reference').addClass('invisible');
        }

        $(template).find('.comment-text').text(comment.text);

        return template;
    }

    function deleteComment() {
        var commentPanel = $(this).closest('.comment-panel');
        var targetId = commentPanel.attr('id').replace('comment-', '');
        $.ajax({
            url: Urls.COMMENTS_DETAIL.replace(Urls.PK_MASK, targetId),
            type: 'DELETE',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            },
            success: function (result) {
                delete comments[targetId];
                commentPanel.remove();
            },
            error: function (result) {
                alert(result.responseText);
            }
        });
    }

    function reply() {
        var commentPanel = $(this).closest('.comment-panel');
        var targetId = commentPanel.attr('id').replace('comment-', '');

        var newCommentPanel = $('#new-comment');
        var parentCommentLink = newCommentPanel.find('.parent-comment-link');
        parentCommentLink.attr('href', '#comment-' + targetId);
        parentCommentLink.text(comments[targetId].author.username);
        parentCommentLink.click(highlightCommentOnClick);
        newCommentPanel.find('.parent-comment-reference').removeClass('invisible');

        newCommentPanel.effect("highlight", {color: '#ffc060'}, 1500);
        window.location.hash = '#new-comment';
    }

    function clearRecipient() {
        var newCommentPanel = '#new-comment';
        $(newCommentPanel).find('.parent-comment-link').removeAttr('href');
        $(newCommentPanel).find('.parent-comment-reference').addClass('invisible');
    }

    function addNewComment() {
        var comment = new CommentModel({});
        comment.text = $('#new-comment-text').val();
        var parentCommentRef = $('#new-comment-form').find('.parent-comment-link').attr('href');
        comment.parentCommentId = parentCommentRef ? parentCommentRef.replace('#comment-', '') : null;

        $.ajax({
                url: Urls.COMMENTS_LIST,
                data: {
                    text: comment.text, 'parent_comment': comment.parentCommentId, 'post': postId
                },
                type: 'POST',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
                },
                success: function (result) {
                    addCommentItem(result);

                    $('#new-comment-text').val('');
                    clearRecipient();
                    $('#no-comments-placeholder').addClass('invisible');

                    var freshComponent = $('#comment-' + result.id);
                    highlightComment(freshComponent);
                    freshComponent.addClass('fresh');

                    window.location.hash = '#comment-' + result.id;
                }
                ,
                error: function (result) {
                    alert(result.responseText);
                }
            }
        );

        return false;
    }
})
;

function CommentModel(data) {
    var self = this;

    self.id = data.id ? data.id : null;
    self.text = data.text ? data.text : null;
    self.author = data.author ? data.author : null;
    self.createdAt = data.created_at ? new Date(data.created_at) : null;
    self.parentCommentId = data.parent_comment ? data.parent_comment : null;

    self.getCreatedAtString = function () {
        if (!self.createdAt) {
            return null;
        }
        var dateString = getDateString(self.createdAt);
        var timeString = getTimeString(self.createdAt);
        return dateString == getDateString(new Date())
            ? timeString
            : dateString + " " + timeString;
    };

    function getDateString(d) {
        return ("0" + d.getDate()).slice(-2) + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" +
            d.getFullYear();
    }

    function getTimeString(d) {
        return ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
    }

}