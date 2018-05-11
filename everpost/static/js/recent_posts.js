$(function () {
    posts = {};
    currentDate = null;
    dateChanged = false;

    init();
    changePostsDate();

    function init() {
        currentDate = getDateString(new Date());

        $('.load-more').click(loadPosts);
        $('.input-date').val(currentDate);
        $('#date-select-form').submit(changePostsDate);
    }

    function changePostsDate() {
        currentDate = $('.input-date').val();
        if (!currentDate.match(/^(\d{1,2})-(\d{1,2})-(\d{4})$/)) {
            return false;
        }
        Urls.MORE_POSTS = Urls.MORE_POSTS_TEMPLATE.replace(Urls.DATE_MASK, currentDate);
        dateChanged = true;
        loadPosts();
        return false;
    }

    function loadPosts() {
        $.get(Urls.MORE_POSTS, function (data) {
            if (dateChanged) {
                posts = {};
                $("#posts-panel").empty();
                dateChanged = false;
            }

            for (var i = 0; i < data.length; i++) {
                var item = data[i];
                addPostItem(item);
            }

            if (Object.keys(posts).length == 0) {
                $('#no-posts-placeholder').removeClass('invisible');
            } else {
                $('#no-posts-placeholder').addClass('invisible');
            }

            $('.loader').addClass('invisible');
            if (data.next == null) {
                $('.load-more').addClass('invisible')
            } else {
                $('.load-more').removeClass('invisible')
            }
            Urls.MORE_POSTS = data.next;

        });
    }


    function addPostItem(item) {
        var post = new PostModel(item);
        if (posts[post.id]) {
            delete posts[post.id];
            $('#post-' + post.id).remove();
        }
        posts[post.id] = post;

        var template = fillPostTemplate(post);
        template.appendTo("#posts-panel");
        template.show();
    }
});

function fillPostTemplate(post) {
    var template = $("#post-template").clone();
    template.attr("id", "post-" + post.id);

    var postTitle = $(template).find('.post-title');
    postTitle.text(post.title);
    postTitle.attr('href', Urls.VIEW_POST.replace(Urls.PK_MASK, post.id));

    var authorLink = $(template).find('.author-link');
    authorLink.text(post.author.username);
    authorLink.attr('href', Urls.USER_POSTS.replace(Urls.PK_MASK, post.author.id));

    $(template).find('.post-time').text(post.getCreatedAtString());

    return template;
}

function getDateString(d) {
    return ("0" + d.getDate()).slice(-2) + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" +
        d.getFullYear();
}

function PostModel(data) {
    self = this;
    self.id = data.id ? data.id : null;
    self.title = data.title ? data.title : null;
    self.author = data.author ? data.author : null;
    self.createdAt = data.created_at ? new Date(data.created_at) : null;

    self.getCreatedAtString = function () {
        if (!self.createdAt) {
            return null;
        }
        return getTimeString(self.createdAt);
    };

    function getTimeString(d) {
        return ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
    }
}