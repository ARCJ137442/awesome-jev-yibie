#!/usr/bin/env bash
# merge-prs.sh — 依次合并 awesome-jev 的贡献者 PR。
#
# 用法:
#   scripts/maintainer/merge-prs.sh 84 85 86     # 指定 PR 号
#   scripts/maintainer/merge-prs.sh              # 默认处理全部 open PR
#
# 为什么需要脚本：每个 PR 都要改 README.md 里【相邻的计数行】，第二个 PR 起必然冲突；
# 而且 README.md 是生成物，不能手工解冲突。手工 rebase 十几个 PR 不现实。
#
# 踩过的坑（改动前请先读）:
#   1. fork 仓库名不统一（awesome-jev / awesome-jev-yibie / yibie_awesome-jev / awesome-jev-1），
#      必须用 headRepository.nameWithOwner，不能拼 /awesome-jev。
#   2. rebase 前必须先把本地 main 拉到 origin/main，否则会 rebase 到过期基线，
#      推回 fork 后 PR 依然显示 CONFLICTING。
#   3. 一个 PR 可能有多个提交（先加条目、再改措辞），会产生【多轮】冲突；
#      只解一轮会让 `rebase --continue` 失败。必须循环处理。
#   4. `grep -qF "$line"` 中条目以 "- [" 开头，会被当成选项 → 必须写 `grep -qF -- "$line"`。
#   5. 【最隐蔽】rebase 之后、合并之前，main 可能又被别的 PR 推进了。此时我们推上去的
#      分支相对新 main 会【少掉那条刚合并的条目】—— 等于撤销别人的合并，GitHub 因此拒绝合并。
#      修法：合并失败就重新同步 main，把整个 rebase+push+merge 再走一轮（最多 3 轮）。
#   6. 批量跑几十个 PR 时 `gh` 偶发返回空（限流或瞬时故障），脚本里 `2>/dev/null` 会把原因藏掉。
#      失败项直接重跑本脚本即可，不要以为是权限问题。
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT" || exit 1

PRS=("$@")
if [ ${#PRS[@]} -eq 0 ]; then
  mapfile -t PRS < <(gh pr list --state open --limit 100 --json number -q '.[].number' | sort -n)
fi
[ ${#PRS[@]} -eq 0 ] && { echo "没有 open PR"; exit 0; }

info() { echo "  $*"; }

sync_main() {
  git checkout -q main 2>/dev/null
  git rebase --abort >/dev/null 2>&1
  git checkout -q main 2>/dev/null || return 1
  git fetch -q origin main 2>/dev/null
  git merge -q --ff-only origin/main 2>/dev/null || git reset -q --hard origin/main
}

wait_mergeable() {
  local n="$1" st
  for _ in $(seq 1 10); do
    st=$(gh pr view "$n" --json mergeable -q .mergeable 2>/dev/null)
    [ "$st" = "MERGEABLE" ] && return 0
    sleep 3
  done
  return 1
}

# 安全网：有的 PR 只改分类文件、不碰 README.md，会【干净合并】但把首页计数留在旧值。
sync_readme() {
  git checkout -q main 2>/dev/null
  git fetch -q origin main 2>/dev/null
  git merge -q --ff-only origin/main 2>/dev/null || git reset -q --hard origin/main
  python3 scripts/build-readme.py >/dev/null 2>&1 || return 0
  if [ -n "$(git status --short)" ]; then
    git add -A
    git commit -q -m "chore: rebuild README after PR merge" 2>/dev/null \
      && git push -q origin main 2>/dev/null \
      && info "README 计数已补建并推送"
  fi
}

# 解当前一轮冲突：README 重新生成，分类文件保留 main 侧并补上本 PR 的条目行
resolve_round() {
  local n="$1" added conflicted
  added=$(gh pr diff "$n" 2>/dev/null | grep -E '^\+- \[[^]]+\]\(https?://' | head -1 | sed 's/^+//')
  conflicted=$(git diff --name-only --diff-filter=U)
  [ -z "$conflicted" ] && return 1
  for f in $conflicted; do
    [ "$f" = "README.md" ] && continue
    git checkout --ours -- "$f" 2>/dev/null
    if [ -n "$added" ] && ! grep -qF -- "$added" "$f" 2>/dev/null; then
      printf '%s\n' "$added" >>"$f"
    fi
    git add "$f"
    info "冲突已解: $f"
  done
  python3 scripts/build-readme.py >/dev/null 2>&1 || true
  git add -A
  return 0
}

# rebase 到 main → 推回 fork → 合并。成功返回 0。
rebase_push_merge() {
  local n="$1" fork="$2" branch="$3" round=0 remote url

  git fetch -q -f origin "pull/$n/head:pr$n" || { info "✗ 取不到 PR 分支"; return 1; }
  git checkout -q "pr$n" || { info "✗ 切分支失败"; return 1; }
  git reset -q --hard "pr$n"

  git rebase main >/dev/null 2>&1
  while [ $round -lt 8 ]; do
    [ -z "$(git diff --name-only --diff-filter=U 2>/dev/null)" ] && break
    round=$((round + 1))
    resolve_round "$n" || break
    GIT_EDITOR=true git rebase --continue >/dev/null 2>&1 || true
  done
  if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
    if [ -z "$(git diff --name-only --diff-filter=U 2>/dev/null)" ]; then
      GIT_EDITOR=true git rebase --continue >/dev/null 2>&1 \
        || GIT_EDITOR=true git rebase --skip >/dev/null 2>&1
    fi
  fi
  if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
    info "✗ rebase 未完成"; git rebase --abort >/dev/null 2>&1; return 1
  fi
  info "rebase 完成（${round} 轮冲突）"

  remote="fork-$(echo "$fork" | tr '/' '-')"
  url="git@github.com:$fork.git"
  git remote get-url "$remote" >/dev/null 2>&1 || git remote add "$remote" "$url"
  git remote set-url "$remote" "$url"
  git fetch -q "$remote" "$branch" 2>/dev/null
  if git push -q --force-with-lease "$remote" "pr$n:$branch" 2>/dev/null \
     || git push -q --force "$remote" "pr$n:$branch" 2>/dev/null; then
    info "已推回 $fork/$branch"
  else
    info "✗ 推送失败（可能无权限或 fork 已删）"; return 1
  fi

  if wait_mergeable "$n" && gh pr merge "$n" --merge \
      --subject "Merge pull request #$n from $fork" >/dev/null 2>&1; then
    info "✓ rebase 后合并"
    return 0
  fi
  info "✗ 合并失败（多为 main 又前进了）"
  return 1
}

for n in "${PRS[@]}"; do
  echo "=== PR #$n ==="
  read -r fork branch <<<"$(gh pr view "$n" --json headRepository,headRefName \
      -q '.headRepository.nameWithOwner + " " + .headRefName' 2>/dev/null)"
  if [ -z "${fork:-}" ]; then
    sleep 3
    read -r fork branch <<<"$(gh pr view "$n" --json headRepository,headRefName \
        -q '.headRepository.nameWithOwner + " " + .headRefName' 2>/dev/null)"
  fi
  [ -z "${fork:-}" ] && { info "✗ 取不到 PR 信息（gh 瞬时故障），请重跑本脚本"; continue; }
  info "fork=$fork branch=$branch"

  sync_main || { info "✗ main 同步失败"; continue; }

  if wait_mergeable "$n"; then
    if gh pr merge "$n" --merge --subject "Merge pull request #$n from $fork" >/dev/null 2>&1; then
      info "✓ 直接合并"
      sync_readme
      continue
    fi
    info "直接合并失败，转 rebase"
  else
    info "不可直接合并，走 rebase"
  fi

  # 最多 3 轮：每轮重新同步 main，避免推到过期基线而回退别人的合并
  for attempt in 1 2 3; do
    rebase_push_merge "$n" "$fork" "$branch" && { sync_readme; break; }
    [ "$attempt" -lt 3 ] && { info "重试 $attempt/3：重新同步 main"; sync_main; }
  done
done

sync_main
echo ""
echo "=== 收尾 ==="
git log --oneline -1
echo "剩余 open: $(gh pr list --state open --json number -q '[.[].number] | join(",")')"
python3 - <<'PY'
import re
t = open('README.md').read()
seg = t.split('## Current coverage')[1].split('Each entry lives')[0]
print("条目总数:", sum(int(m) for m in re.findall(r'— (\d+) entr', seg)))
PY
