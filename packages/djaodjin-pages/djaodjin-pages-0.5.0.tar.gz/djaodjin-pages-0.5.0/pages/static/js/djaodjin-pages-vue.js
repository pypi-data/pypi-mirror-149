

Vue.component('editables-list', {
    mixins: [
        itemListMixin
    ],
    data: function() {
        return {
            url: this.$urls.api_content,
            params: {
                o: '-created_at'
            },
            newItem: {title: ""},
            nbItemsPerRow: 2,
        }
    },
    methods: {
        create: function() {
            var vm = this;
            vm.reqPost(vm.url,{title: vm.newItem.title},
            function success(resp, textStatus, jqXHR) {
                var location = jqXHR.getResponseHeader('Location');
                if( location ) {
                    window.location = location;
                }
            });
            return false;
        },
    },
    computed: {
        nbRows: function() {
            var vm = this;
            const nbFullRows = Math.floor(
                vm.items.results.length / vm.nbItemsPerRow);
            return vm.items.results.length % vm.nbItemsPerRow == 0 ?
                nbFullRows : nbFullRows + 1;
        },
    },
    mounted: function(){
        this.get();
    }
});


Vue.component('editables-detail', {
    mixins: [
        itemMixin
    ],
    data: function() {
        return {
            url: this.$urls.api_content,
            tags: [],
            isFollowing: false,
            nbFollowers: 0,
            isUpVote: 0,
            nbUpVotes: 0,
            comments: {count: 0, results: []},
            message: "",
            newItem: {title: ""},
        }
    },
    methods: {
        // functions available to editors
        create: function() {
            var vm = this;
            vm.reqPost(vm.url,{title: vm.newItem.title},
            function success(resp, textStatus, jqXHR) {
                var location = jqXHR.getResponseHeader('Location');
                if( location ) {
                    window.location = location;
                }
            });
            return false;
        },
        // functions available to readers
        submitFollow: function() {
            var vm = this;
            vm.reqPost(vm.isFollowing ? this.$urls.api_unfollow
                       : this.$urls.api_follow,
                function success(resp) {
                    vm.isFollowing = !vm.isFollowing;
                    vm.nbFollowers += vm.isFollowing ? 1 : -1;
            });
            return false;
        },
        submitVote: function() {
            var vm = this;
            vm.reqPost(vm.isUpVote ? this.$urls.api_downvote
                       : this.$urls.api_upvote,
                function success(resp) {
                    vm.isUpVote = !vm.isUpVote;
                    vm.nbUpVotes += vm.isUpVote ? 1 : -1;
            });
            return false;
        },
        submitComment: function() {
            var vm = this;
            vm.reqPost(this.$urls.api_comments, {
                text: vm.message},
            function success(resp) {
                vm.message = "";
                vm.comments.results.push(resp);
                vm.comments.count += 1;
            });
            return 0;
        },
    },
    mounted: function() {
        var vm = this;
        vm.get(function success(resp) {
            vm.isFollowing = resp.data.is_following;
            vm.nbFollowers = resp.data.nb_followers;
            vm.isUpVote = resp.data.is_upvote;
            vm.nbUpVotes = resp.data.nb_upvotes;
            if( resp.data.extra && resp.data.extra.tags ) {
                vm.tags = resp.data.extra.tags;
            }
        });
        vm.reqGet(this.$urls.api_comments,
        function success(resp) {
            vm.comments = resp;
        });
    }
});
