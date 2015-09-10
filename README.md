# robot-baby

> TODO: Add accurate description & references (papers, etc)

### Developer documentation

We have two main branches, master and develop.

For every new feature we create a new branch in the following form:

```sh
git checkout -b new_feature
```

After we are done developing, we test, and make a pull request to the develop branch via the Github UI. If there are merging conflicts, git will detect them and will not allow the branches to merge. We resolve the conflicts in the following way:

```sh
git merge --no-commit --no-ff -s recursive -X patience origin/develop
```

After the conflicts are resolved:

```sh
git commit -v
git push origin new_feature
```

When we are absolutely sure that no changes will break the master branch, we publish.

> Related documentation:

> https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

> http://nvie.com/posts/a-successful-git-branching-model/

### Modules

> TODO: Add modules
