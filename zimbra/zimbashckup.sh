




<!DOCTYPE html>
<html>
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>zimbashckup/zimbashckup.sh at master · davromaniak/zimbashckup · GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png" />
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png" />
    <meta property="fb:app_id" content="1401488693436528"/>

      <meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="davromaniak/zimbashckup" name="twitter:title" /><meta content="zimbashckup - ZimBashckup : Zimbra Backup Script in Bash" name="twitter:description" /><meta content="https://1.gravatar.com/avatar/92dbba5d2b4151786de9eb2bf9696790?d=https%3A%2F%2Fidenticons.github.com%2Fbac1b97407c431ce149ab6f8b424868e.png&amp;r=x&amp;s=400" name="twitter:image:src" />
<meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="https://1.gravatar.com/avatar/92dbba5d2b4151786de9eb2bf9696790?d=https%3A%2F%2Fidenticons.github.com%2Fbac1b97407c431ce149ab6f8b424868e.png&amp;r=x&amp;s=400" property="og:image" /><meta content="davromaniak/zimbashckup" property="og:title" /><meta content="https://github.com/davromaniak/zimbashckup" property="og:url" /><meta content="zimbashckup - ZimBashckup : Zimbra Backup Script in Bash" property="og:description" />

    <meta name="hostname" content="github-fe137-cp1-prd.iad.github.net">
    <meta name="ruby" content="ruby 2.1.0p0-github-tcmalloc (87d8860372) [x86_64-linux]">
    <link rel="assets" href="https://github.global.ssl.fastly.net/">
    <link rel="conduit-xhr" href="https://ghconduit.com:25035/">
    <link rel="xhr-socket" href="/_sockets" />


    <meta name="msapplication-TileImage" content="/windows-tile.png" />
    <meta name="msapplication-TileColor" content="#ffffff" />
    <meta name="selected-link" value="repo_source" data-pjax-transient />
    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="4EC0A27A:1496:4845708:52FD4D2E" name="octolytics-dimension-request_id" />
    

    
    
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />

    <meta content="authenticity_token" name="csrf-param" />
<meta content="zccUpLRJy1bamJ7ssrh9Py7yP9ZnMifw0GxuxcnsOTQ=" name="csrf-token" />

    <link href="https://github.global.ssl.fastly.net/assets/github-fdc2288b41d96b84d72e1f10a66b76dc179afa0c.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://github.global.ssl.fastly.net/assets/github2-27f5b26611be5538d65fc5fe2cceffaefb64a961.css" media="all" rel="stylesheet" type="text/css" />
    
    


      <script src="https://github.global.ssl.fastly.net/assets/frameworks-693e11922dcacc3a7408a911fe1647da4febd3bd.js" type="text/javascript"></script>
      <script async="async" defer="defer" src="https://github.global.ssl.fastly.net/assets/github-b530fe2b2cf096324b42235641930856f9a32327.js" type="text/javascript"></script>
      
      <meta http-equiv="x-pjax-version" content="809137c120d8b289df8c183f9d9c045c">

        <link data-pjax-transient rel='permalink' href='/davromaniak/zimbashckup/blob/2c223b0e267f86583615d7c20d2096cf4f63da4f/zimbashckup.sh'>

  <meta name="description" content="zimbashckup - ZimBashckup : Zimbra Backup Script in Bash" />

  <meta content="298836" name="octolytics-dimension-user_id" /><meta content="davromaniak" name="octolytics-dimension-user_login" /><meta content="15436612" name="octolytics-dimension-repository_id" /><meta content="davromaniak/zimbashckup" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="15436612" name="octolytics-dimension-repository_network_root_id" /><meta content="davromaniak/zimbashckup" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/davromaniak/zimbashckup/commits/master.atom" rel="alternate" title="Recent Commits to zimbashckup:master" type="application/atom+xml" />

  </head>


  <body class="logged_out  env-production linux vis-public page-blob tipsy-tooltips">
    <div class="wrapper">
      
      
      
      


      
      <div class="header header-logged-out">
  <div class="container clearfix">

    <a class="header-logo-wordmark" href="https://github.com/">
      <span class="mega-octicon octicon-logo-github"></span>
    </a>

    <div class="header-actions">
        <a class="button primary" href="/join">Sign up</a>
      <a class="button signin" href="/login?return_to=%2Fdavromaniak%2Fzimbashckup%2Fblob%2Fmaster%2Fzimbashckup.sh">Sign in</a>
    </div>

    <div class="command-bar js-command-bar  in-repository">

      <ul class="top-nav">
          <li class="explore"><a href="/explore">Explore</a></li>
        <li class="features"><a href="/features">Features</a></li>
          <li class="enterprise"><a href="https://enterprise.github.com/">Enterprise</a></li>
          <li class="blog"><a href="/blog">Blog</a></li>
      </ul>
        <form accept-charset="UTF-8" action="/search" class="command-bar-form" id="top_search_form" method="get">

<input type="text" data-hotkey="/ s" name="q" id="js-command-bar-field" placeholder="Search or type a command" tabindex="1" autocapitalize="off"
    
    
      data-repo="davromaniak/zimbashckup"
      data-branch="master"
      data-sha="a508f07bb6161a9e498703e6d057fbe40827c3fe"
  >

    <input type="hidden" name="nwo" value="davromaniak/zimbashckup" />

    <div class="select-menu js-menu-container js-select-menu search-context-select-menu">
      <span class="minibutton select-menu-button js-menu-target">
        <span class="js-select-button">This repository</span>
      </span>

      <div class="select-menu-modal-holder js-menu-content js-navigation-container">
        <div class="select-menu-modal">

          <div class="select-menu-item js-navigation-item js-this-repository-navigation-item selected">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" class="js-search-this-repository" name="search_target" value="repository" checked="checked" />
            <div class="select-menu-item-text js-select-button-text">This repository</div>
          </div> <!-- /.select-menu-item -->

          <div class="select-menu-item js-navigation-item js-all-repositories-navigation-item">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" name="search_target" value="global" />
            <div class="select-menu-item-text js-select-button-text">All repositories</div>
          </div> <!-- /.select-menu-item -->

        </div>
      </div>
    </div>

  <span class="octicon help tooltipped downwards" aria-label="Show command bar help">
    <span class="octicon octicon-question"></span>
  </span>


  <input type="hidden" name="ref" value="cmdform">

</form>
    </div>

  </div>
</div>




          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        

<ul class="pagehead-actions">


  <li>
    <a href="/login?return_to=%2Fdavromaniak%2Fzimbashckup"
    class="minibutton with-count js-toggler-target star-button tooltipped upwards"
    aria-label="You must be signed in to use this feature" rel="nofollow">
    <span class="octicon octicon-star"></span>Star
  </a>

    <a class="social-count js-social-count" href="/davromaniak/zimbashckup/stargazers">
      2
    </a>

  </li>

    <li>
      <a href="/login?return_to=%2Fdavromaniak%2Fzimbashckup"
        class="minibutton with-count js-toggler-target fork-button tooltipped upwards"
        aria-label="You must be signed in to fork a repository" rel="nofollow">
        <span class="octicon octicon-git-branch"></span>Fork
      </a>
      <a href="/davromaniak/zimbashckup/network" class="social-count">
        0
      </a>
    </li>
</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="repo-label"><span>public</span></span>
          <span class="mega-octicon octicon-repo"></span>
          <span class="author">
            <a href="/davromaniak" class="url fn" itemprop="url" rel="author"><span itemprop="title">davromaniak</span></a>
          </span>
          <span class="repohead-name-divider">/</span>
          <strong><a href="/davromaniak/zimbashckup" class="js-current-repository js-repo-home-link">zimbashckup</a></strong>

          <span class="page-context-loader">
            <img alt="Octocat-spinner-32" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">
      

      <div class="repository-with-sidebar repo-container new-discussion-timeline js-new-discussion-timeline  ">
        <div class="repository-sidebar clearfix">
            

<div class="sunken-menu vertical-right repo-nav js-repo-nav js-repository-container-pjax js-octicon-loaders">
  <div class="sunken-menu-contents">
    <ul class="sunken-menu-group">
      <li class="tooltipped leftwards" aria-label="Code">
        <a href="/davromaniak/zimbashckup" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-gotokey="c" data-pjax="true" data-selected-links="repo_source repo_downloads repo_commits repo_tags repo_branches /davromaniak/zimbashckup">
          <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

        <li class="tooltipped leftwards" aria-label="Issues">
          <a href="/davromaniak/zimbashckup/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="i" data-selected-links="repo_issues /davromaniak/zimbashckup/issues">
            <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
            <span class='counter'>0</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>

      <li class="tooltipped leftwards" aria-label="Pull Requests">
        <a href="/davromaniak/zimbashckup/pulls" aria-label="Pull Requests" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="p" data-selected-links="repo_pulls /davromaniak/zimbashckup/pulls">
            <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull Requests</span>
            <span class='counter'>0</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


    </ul>
    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">

      <li class="tooltipped leftwards" aria-label="Pulse">
        <a href="/davromaniak/zimbashckup/pulse" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="pulse /davromaniak/zimbashckup/pulse">
          <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped leftwards" aria-label="Graphs">
        <a href="/davromaniak/zimbashckup/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_graphs repo_contributors /davromaniak/zimbashckup/graphs">
          <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped leftwards" aria-label="Network">
        <a href="/davromaniak/zimbashckup/network" aria-label="Network" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-selected-links="repo_network /davromaniak/zimbashckup/network">
          <span class="octicon octicon-git-branch"></span> <span class="full-word">Network</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>
    </ul>


  </div>
</div>

              <div class="only-with-full-nav">
                

  

<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone">
  <h3><strong>HTTPS</strong> clone URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/davromaniak/zimbashckup.git" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/davromaniak/zimbashckup.git" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>

  

<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone">
  <h3><strong>Subversion</strong> checkout URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/davromaniak/zimbashckup" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/davromaniak/zimbashckup" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>


<p class="clone-options">You can clone with
      <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>,
      or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <span class="octicon help tooltipped upwards" aria-label="Get help on which URL is right for you.">
    <a href="https://help.github.com/articles/which-remote-url-should-i-use">
    <span class="octicon octicon-question"></span>
    </a>
  </span>
</p>



                <a href="/davromaniak/zimbashckup/archive/master.zip"
                   class="minibutton sidebar-button"
                   title="Download this repository as a zip file"
                   rel="nofollow">
                  <span class="octicon octicon-cloud-download"></span>
                  Download ZIP
                </a>
              </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          


<!-- blob contrib key: blob_contributors:v21:4db768b3df763d39b3ed65b89c8594c0 -->

<p title="This is a placeholder element" class="js-history-link-replace hidden"></p>

<a href="/davromaniak/zimbashckup/find/master" data-pjax data-hotkey="t" class="js-show-file-finder" style="display:none">Show File Finder</a>

<div class="file-navigation">
  

<div class="select-menu js-menu-container js-select-menu" >
  <span class="minibutton select-menu-button js-menu-target" data-hotkey="w"
    data-master-branch="master"
    data-ref="master"
    role="button" aria-label="Switch branches or tags" tabindex="0">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button">master</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax>

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-remove-close js-menu-close"></span>
      </div> <!-- /.select-menu-header -->

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div><!-- /.select-menu-tabs -->
      </div><!-- /.select-menu-filters -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item selected">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/davromaniak/zimbashckup/blob/master/zimbashckup.sh"
                 data-name="master"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="master">master</a>
            </div> <!-- /.select-menu-item -->
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

    </div> <!-- /.select-menu-modal -->
  </div> <!-- /.select-menu-modal-holder -->
</div> <!-- /.select-menu -->

  <div class="breadcrumb">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/davromaniak/zimbashckup" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">zimbashckup</span></a></span></span><span class="separator"> / </span><strong class="final-path">zimbashckup.sh</strong> <span class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="zimbashckup.sh" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>


  <div class="commit file-history-tease">
    <img alt="Cyril LAVIER" class="main-avatar js-avatar" data-user="298836" height="24" src="https://2.gravatar.com/avatar/92dbba5d2b4151786de9eb2bf9696790?d=https%3A%2F%2Fidenticons.github.com%2Fbac1b97407c431ce149ab6f8b424868e.png&amp;r=x&amp;s=140" width="24" />
    <span class="author"><a href="/davromaniak" rel="author">davromaniak</a></span>
    <time class="js-relative-date" data-title-format="YYYY-MM-DD HH:mm:ss" datetime="2013-12-27T10:19:05-08:00" title="2013-12-27 10:19:05">December 27, 2013</time>
    <div class="commit-title">
        <a href="/davromaniak/zimbashckup/commit/eab5ea196a7ef6306eabeffc722352f6cc0081b7" class="message" data-pjax="true" title="- Corrected the filename when doing a united backup.

- Added backup of mail filters in sieve format.">- Corrected the filename when doing a united backup.</a>
    </div>

    <div class="participation">
      <p class="quickstat"><a href="#blob_contributors_box" rel="facebox"><strong>1</strong> contributor</a></p>
      
    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
          <li class="facebox-user-list-item">
            <img alt="Cyril LAVIER" class=" js-avatar" data-user="298836" height="24" src="https://2.gravatar.com/avatar/92dbba5d2b4151786de9eb2bf9696790?d=https%3A%2F%2Fidenticons.github.com%2Fbac1b97407c431ce149ab6f8b424868e.png&amp;r=x&amp;s=140" width="24" />
            <a href="/davromaniak">davromaniak</a>
          </li>
      </ul>
    </div>
  </div>

<div class="file-box">
  <div class="file">
    <div class="meta clearfix">
      <div class="info file-name">
        <span class="icon"><b class="octicon octicon-file-text"></b></span>
        <span class="mode" title="File Mode">executable file</span>
        <span class="meta-divider"></span>
          <span>238 lines (228 sloc)</span>
          <span class="meta-divider"></span>
        <span>6.89 kb</span>
      </div>
      <div class="actions">
        <div class="button-group">
              <a class="minibutton disabled tooltipped leftwards" href="#"
                 aria-label="You must be signed in to make or propose changes">Edit</a>
          <a href="/davromaniak/zimbashckup/raw/master/zimbashckup.sh" class="button minibutton " id="raw-url">Raw</a>
            <a href="/davromaniak/zimbashckup/blame/master/zimbashckup.sh" class="button minibutton js-update-url-with-hash">Blame</a>
          <a href="/davromaniak/zimbashckup/commits/master/zimbashckup.sh" class="button minibutton " rel="nofollow">History</a>
        </div><!-- /.button-group -->
          <a class="minibutton danger disabled empty-icon tooltipped leftwards" href="#"
             aria-label="You must be signed in to make or propose changes">
          Delete
        </a>
      </div><!-- /.actions -->
    </div>
        <div class="blob-wrapper data type-shell js-blob-data">
        <table class="file-code file-diff tab-size-8">
          <tr class="file-code-line">
            <td class="blob-line-nums">
              <span id="L1" rel="#L1">1</span>
<span id="L2" rel="#L2">2</span>
<span id="L3" rel="#L3">3</span>
<span id="L4" rel="#L4">4</span>
<span id="L5" rel="#L5">5</span>
<span id="L6" rel="#L6">6</span>
<span id="L7" rel="#L7">7</span>
<span id="L8" rel="#L8">8</span>
<span id="L9" rel="#L9">9</span>
<span id="L10" rel="#L10">10</span>
<span id="L11" rel="#L11">11</span>
<span id="L12" rel="#L12">12</span>
<span id="L13" rel="#L13">13</span>
<span id="L14" rel="#L14">14</span>
<span id="L15" rel="#L15">15</span>
<span id="L16" rel="#L16">16</span>
<span id="L17" rel="#L17">17</span>
<span id="L18" rel="#L18">18</span>
<span id="L19" rel="#L19">19</span>
<span id="L20" rel="#L20">20</span>
<span id="L21" rel="#L21">21</span>
<span id="L22" rel="#L22">22</span>
<span id="L23" rel="#L23">23</span>
<span id="L24" rel="#L24">24</span>
<span id="L25" rel="#L25">25</span>
<span id="L26" rel="#L26">26</span>
<span id="L27" rel="#L27">27</span>
<span id="L28" rel="#L28">28</span>
<span id="L29" rel="#L29">29</span>
<span id="L30" rel="#L30">30</span>
<span id="L31" rel="#L31">31</span>
<span id="L32" rel="#L32">32</span>
<span id="L33" rel="#L33">33</span>
<span id="L34" rel="#L34">34</span>
<span id="L35" rel="#L35">35</span>
<span id="L36" rel="#L36">36</span>
<span id="L37" rel="#L37">37</span>
<span id="L38" rel="#L38">38</span>
<span id="L39" rel="#L39">39</span>
<span id="L40" rel="#L40">40</span>
<span id="L41" rel="#L41">41</span>
<span id="L42" rel="#L42">42</span>
<span id="L43" rel="#L43">43</span>
<span id="L44" rel="#L44">44</span>
<span id="L45" rel="#L45">45</span>
<span id="L46" rel="#L46">46</span>
<span id="L47" rel="#L47">47</span>
<span id="L48" rel="#L48">48</span>
<span id="L49" rel="#L49">49</span>
<span id="L50" rel="#L50">50</span>
<span id="L51" rel="#L51">51</span>
<span id="L52" rel="#L52">52</span>
<span id="L53" rel="#L53">53</span>
<span id="L54" rel="#L54">54</span>
<span id="L55" rel="#L55">55</span>
<span id="L56" rel="#L56">56</span>
<span id="L57" rel="#L57">57</span>
<span id="L58" rel="#L58">58</span>
<span id="L59" rel="#L59">59</span>
<span id="L60" rel="#L60">60</span>
<span id="L61" rel="#L61">61</span>
<span id="L62" rel="#L62">62</span>
<span id="L63" rel="#L63">63</span>
<span id="L64" rel="#L64">64</span>
<span id="L65" rel="#L65">65</span>
<span id="L66" rel="#L66">66</span>
<span id="L67" rel="#L67">67</span>
<span id="L68" rel="#L68">68</span>
<span id="L69" rel="#L69">69</span>
<span id="L70" rel="#L70">70</span>
<span id="L71" rel="#L71">71</span>
<span id="L72" rel="#L72">72</span>
<span id="L73" rel="#L73">73</span>
<span id="L74" rel="#L74">74</span>
<span id="L75" rel="#L75">75</span>
<span id="L76" rel="#L76">76</span>
<span id="L77" rel="#L77">77</span>
<span id="L78" rel="#L78">78</span>
<span id="L79" rel="#L79">79</span>
<span id="L80" rel="#L80">80</span>
<span id="L81" rel="#L81">81</span>
<span id="L82" rel="#L82">82</span>
<span id="L83" rel="#L83">83</span>
<span id="L84" rel="#L84">84</span>
<span id="L85" rel="#L85">85</span>
<span id="L86" rel="#L86">86</span>
<span id="L87" rel="#L87">87</span>
<span id="L88" rel="#L88">88</span>
<span id="L89" rel="#L89">89</span>
<span id="L90" rel="#L90">90</span>
<span id="L91" rel="#L91">91</span>
<span id="L92" rel="#L92">92</span>
<span id="L93" rel="#L93">93</span>
<span id="L94" rel="#L94">94</span>
<span id="L95" rel="#L95">95</span>
<span id="L96" rel="#L96">96</span>
<span id="L97" rel="#L97">97</span>
<span id="L98" rel="#L98">98</span>
<span id="L99" rel="#L99">99</span>
<span id="L100" rel="#L100">100</span>
<span id="L101" rel="#L101">101</span>
<span id="L102" rel="#L102">102</span>
<span id="L103" rel="#L103">103</span>
<span id="L104" rel="#L104">104</span>
<span id="L105" rel="#L105">105</span>
<span id="L106" rel="#L106">106</span>
<span id="L107" rel="#L107">107</span>
<span id="L108" rel="#L108">108</span>
<span id="L109" rel="#L109">109</span>
<span id="L110" rel="#L110">110</span>
<span id="L111" rel="#L111">111</span>
<span id="L112" rel="#L112">112</span>
<span id="L113" rel="#L113">113</span>
<span id="L114" rel="#L114">114</span>
<span id="L115" rel="#L115">115</span>
<span id="L116" rel="#L116">116</span>
<span id="L117" rel="#L117">117</span>
<span id="L118" rel="#L118">118</span>
<span id="L119" rel="#L119">119</span>
<span id="L120" rel="#L120">120</span>
<span id="L121" rel="#L121">121</span>
<span id="L122" rel="#L122">122</span>
<span id="L123" rel="#L123">123</span>
<span id="L124" rel="#L124">124</span>
<span id="L125" rel="#L125">125</span>
<span id="L126" rel="#L126">126</span>
<span id="L127" rel="#L127">127</span>
<span id="L128" rel="#L128">128</span>
<span id="L129" rel="#L129">129</span>
<span id="L130" rel="#L130">130</span>
<span id="L131" rel="#L131">131</span>
<span id="L132" rel="#L132">132</span>
<span id="L133" rel="#L133">133</span>
<span id="L134" rel="#L134">134</span>
<span id="L135" rel="#L135">135</span>
<span id="L136" rel="#L136">136</span>
<span id="L137" rel="#L137">137</span>
<span id="L138" rel="#L138">138</span>
<span id="L139" rel="#L139">139</span>
<span id="L140" rel="#L140">140</span>
<span id="L141" rel="#L141">141</span>
<span id="L142" rel="#L142">142</span>
<span id="L143" rel="#L143">143</span>
<span id="L144" rel="#L144">144</span>
<span id="L145" rel="#L145">145</span>
<span id="L146" rel="#L146">146</span>
<span id="L147" rel="#L147">147</span>
<span id="L148" rel="#L148">148</span>
<span id="L149" rel="#L149">149</span>
<span id="L150" rel="#L150">150</span>
<span id="L151" rel="#L151">151</span>
<span id="L152" rel="#L152">152</span>
<span id="L153" rel="#L153">153</span>
<span id="L154" rel="#L154">154</span>
<span id="L155" rel="#L155">155</span>
<span id="L156" rel="#L156">156</span>
<span id="L157" rel="#L157">157</span>
<span id="L158" rel="#L158">158</span>
<span id="L159" rel="#L159">159</span>
<span id="L160" rel="#L160">160</span>
<span id="L161" rel="#L161">161</span>
<span id="L162" rel="#L162">162</span>
<span id="L163" rel="#L163">163</span>
<span id="L164" rel="#L164">164</span>
<span id="L165" rel="#L165">165</span>
<span id="L166" rel="#L166">166</span>
<span id="L167" rel="#L167">167</span>
<span id="L168" rel="#L168">168</span>
<span id="L169" rel="#L169">169</span>
<span id="L170" rel="#L170">170</span>
<span id="L171" rel="#L171">171</span>
<span id="L172" rel="#L172">172</span>
<span id="L173" rel="#L173">173</span>
<span id="L174" rel="#L174">174</span>
<span id="L175" rel="#L175">175</span>
<span id="L176" rel="#L176">176</span>
<span id="L177" rel="#L177">177</span>
<span id="L178" rel="#L178">178</span>
<span id="L179" rel="#L179">179</span>
<span id="L180" rel="#L180">180</span>
<span id="L181" rel="#L181">181</span>
<span id="L182" rel="#L182">182</span>
<span id="L183" rel="#L183">183</span>
<span id="L184" rel="#L184">184</span>
<span id="L185" rel="#L185">185</span>
<span id="L186" rel="#L186">186</span>
<span id="L187" rel="#L187">187</span>
<span id="L188" rel="#L188">188</span>
<span id="L189" rel="#L189">189</span>
<span id="L190" rel="#L190">190</span>
<span id="L191" rel="#L191">191</span>
<span id="L192" rel="#L192">192</span>
<span id="L193" rel="#L193">193</span>
<span id="L194" rel="#L194">194</span>
<span id="L195" rel="#L195">195</span>
<span id="L196" rel="#L196">196</span>
<span id="L197" rel="#L197">197</span>
<span id="L198" rel="#L198">198</span>
<span id="L199" rel="#L199">199</span>
<span id="L200" rel="#L200">200</span>
<span id="L201" rel="#L201">201</span>
<span id="L202" rel="#L202">202</span>
<span id="L203" rel="#L203">203</span>
<span id="L204" rel="#L204">204</span>
<span id="L205" rel="#L205">205</span>
<span id="L206" rel="#L206">206</span>
<span id="L207" rel="#L207">207</span>
<span id="L208" rel="#L208">208</span>
<span id="L209" rel="#L209">209</span>
<span id="L210" rel="#L210">210</span>
<span id="L211" rel="#L211">211</span>
<span id="L212" rel="#L212">212</span>
<span id="L213" rel="#L213">213</span>
<span id="L214" rel="#L214">214</span>
<span id="L215" rel="#L215">215</span>
<span id="L216" rel="#L216">216</span>
<span id="L217" rel="#L217">217</span>
<span id="L218" rel="#L218">218</span>
<span id="L219" rel="#L219">219</span>
<span id="L220" rel="#L220">220</span>
<span id="L221" rel="#L221">221</span>
<span id="L222" rel="#L222">222</span>
<span id="L223" rel="#L223">223</span>
<span id="L224" rel="#L224">224</span>
<span id="L225" rel="#L225">225</span>
<span id="L226" rel="#L226">226</span>
<span id="L227" rel="#L227">227</span>
<span id="L228" rel="#L228">228</span>
<span id="L229" rel="#L229">229</span>
<span id="L230" rel="#L230">230</span>
<span id="L231" rel="#L231">231</span>
<span id="L232" rel="#L232">232</span>
<span id="L233" rel="#L233">233</span>
<span id="L234" rel="#L234">234</span>
<span id="L235" rel="#L235">235</span>
<span id="L236" rel="#L236">236</span>
<span id="L237" rel="#L237">237</span>

            </td>
            <td class="blob-line-code"><div class="code-body highlight"><pre><div class='line' id='LC1'><span class="c">#!/bin/bash</span></div><div class='line' id='LC2'><span class="c">#  zimbashckup.sh</span></div><div class='line' id='LC3'><span class="c">#  </span></div><div class='line' id='LC4'><span class="c">#  Copyright 2013 Cyril Lavier &lt;bainisteoir@davromaniak.eu&gt;</span></div><div class='line' id='LC5'><span class="c">#  </span></div><div class='line' id='LC6'><span class="c">#  This program is free software; you can redistribute it and/or modify</span></div><div class='line' id='LC7'><span class="c">#  it under the terms of the GNU General Public License as published by</span></div><div class='line' id='LC8'><span class="c">#  the Free Software Foundation; either version 2 of the License, or</span></div><div class='line' id='LC9'><span class="c">#  (at your option) any later version.</span></div><div class='line' id='LC10'><span class="c">#  </span></div><div class='line' id='LC11'><span class="c">#  This program is distributed in the hope that it will be useful,</span></div><div class='line' id='LC12'><span class="c">#  but WITHOUT ANY WARRANTY; without even the implied warranty of</span></div><div class='line' id='LC13'><span class="c">#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the</span></div><div class='line' id='LC14'><span class="c">#  GNU General Public License for more details.</span></div><div class='line' id='LC15'><span class="c">#  </span></div><div class='line' id='LC16'><span class="c">#  You should have received a copy of the GNU General Public License</span></div><div class='line' id='LC17'><span class="c">#  along with this program; if not, write to the Free Software</span></div><div class='line' id='LC18'><span class="c">#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,</span></div><div class='line' id='LC19'><span class="c">#  MA 02110-1301, USA.</span></div><div class='line' id='LC20'><span class="c">#  </span></div><div class='line' id='LC21'><br/></div><div class='line' id='LC22'>usage<span class="o">()</span> <span class="o">{</span></div><div class='line' id='LC23'>	<span class="nb">echo</span> <span class="s2">&quot;USAGE: $0 [OPTIONS]&quot;</span></div><div class='line' id='LC24'>	<span class="nb">echo</span> <span class="s2">&quot;ZimBashckup : Zimbra Backup Script in Bash&quot;</span></div><div class='line' id='LC25'>	<span class="nb">echo</span> <span class="s2">&quot;&quot;</span></div><div class='line' id='LC26'>	<span class="nb">echo</span> -e <span class="s2">&quot; -v | --verbose\t\t\t\t\tVerbose/debug mode, displays the status of the current task running.&quot;</span></div><div class='line' id='LC27'>	<span class="nb">echo</span> -e <span class="s2">&quot; -u | --unite\t\t\t\t\tBackup whole mailbox at the time, default behavior is to backup every folder separately.&quot;</span></div><div class='line' id='LC28'>	<span class="nb">echo</span> -e <span class="s2">&quot; -p [cmd] | --postscript=[cmd]\t\t\tScript/command to launch after the backup.&quot;</span></div><div class='line' id='LC29'>	<span class="nb">echo</span> -e <span class="s2">&quot; -m [mailboxes] | --mailboxes=[mailboxes]\tBackup only this/these mailboxes (each mailbox separated by a space), default behavior is to backup all mailboxes.&quot;</span></div><div class='line' id='LC30'>	<span class="nb">echo</span> -e <span class="s2">&quot; -d [domains] | --domains=[domains]\t\tBackup only mailboxes which belong to this/these domains (each domain separated by a space), default behavior is to backup all mailboxes. Can&#39;t be used with option \&quot;-m | --mailbox\&quot;.&quot;</span></div><div class='line' id='LC31'>	<span class="nb">echo</span> -e <span class="s2">&quot; -f [tar|tgz|zip] | --format=[tar|tgz|zip]\tFormat used to store backups (this is given to zmmailbox getRestURL command). Default is tar&quot;</span></div><div class='line' id='LC32'>	<span class="nb">echo</span> -e <span class="s2">&quot; -V | --version\t\t\t\t\tDisplay version information.&quot;</span></div><div class='line' id='LC33'>	<span class="nb">echo</span> -e <span class="s2">&quot; -c | --changelog\t\t\t\tDisplay changelog information.&quot;</span></div><div class='line' id='LC34'>	<span class="nb">echo</span> -e <span class="s2">&quot; -h | --help\t\t\t\t\tDisplay this help.&quot;</span></div><div class='line' id='LC35'><span class="o">}</span></div><div class='line' id='LC36'><br/></div><div class='line' id='LC37'>changelog<span class="o">()</span> <span class="o">{</span></div><div class='line' id='LC38'>	<span class="nb">echo</span> <span class="s2">&quot;V0.1: December 25th 2013 : First release&quot;</span></div><div class='line' id='LC39'>	<span class="nb">echo</span> <span class="s2">&quot;See the CHANGELOG for more information&quot;</span></div><div class='line' id='LC40'><span class="o">}</span></div><div class='line' id='LC41'><br/></div><div class='line' id='LC42'>version<span class="o">()</span> <span class="o">{</span></div><div class='line' id='LC43'>	<span class="nb">echo</span> <span class="s2">&quot;ZimBashckUP V0.1&quot;</span></div><div class='line' id='LC44'>	<span class="nb">echo</span> <span class="s2">&quot;Written by Cyril Lavier &lt;bainisteoir(at)davromaniak(dot)eu&gt;&quot;</span></div><div class='line' id='LC45'><span class="o">}</span></div><div class='line' id='LC46'><br/></div><div class='line' id='LC47'>echoerror<span class="o">()</span> <span class="o">{</span></div><div class='line' id='LC48'>	<span class="nb">echo</span> <span class="s2">&quot;ERROR : &quot;</span><span class="nv">$*</span> &gt;<span class="p">&amp;</span>2</div><div class='line' id='LC49'><span class="o">}</span></div><div class='line' id='LC50'><br/></div><div class='line' id='LC51'>echoverbose<span class="o">()</span> <span class="o">{</span></div><div class='line' id='LC52'>	<span class="k">if</span> <span class="o">[</span> ! -z <span class="s2">&quot;$VERBOSE&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC53'><span class="k">		</span><span class="nb">echo</span> <span class="s2">&quot;$*&quot;</span></div><div class='line' id='LC54'>	<span class="k">fi</span></div><div class='line' id='LC55'><span class="o">}</span></div><div class='line' id='LC56'><br/></div><div class='line' id='LC57'>checkrequirements<span class="o">()</span> <span class="o">{</span></div><div class='line' id='LC58'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nv">ret</span><span class="o">=</span>0</div><div class='line' id='LC59'>	<span class="k">for </span>i in gawk date<span class="p">;</span> <span class="k">do</span></div><div class='line' id='LC60'><span class="k">		</span>which <span class="nv">$i</span> &gt; /dev/null</div><div class='line' id='LC61'>		<span class="k">if</span> <span class="o">[</span> <span class="nv">$?</span> -gt 0 <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC62'><span class="k">			</span>echoerror <span class="s2">&quot;$i is missing&quot;</span></div><div class='line' id='LC63'>			<span class="nv">ret</span><span class="o">=</span>1</div><div class='line' id='LC64'>		<span class="k">fi</span></div><div class='line' id='LC65'><span class="k">	done</span></div><div class='line' id='LC66'><span class="k">	</span>which zmcontrol &gt; /dev/null</div><div class='line' id='LC67'>	<span class="k">if</span> <span class="o">[</span> <span class="nv">$?</span> -gt 0 <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC68'><span class="k">		</span>echoerror <span class="s2">&quot;zmcontrol is missing, this means you either don&#39;t have Zimbra installed on this server or the PATH variable is not correctly set under the zimbra user account&quot;</span></div><div class='line' id='LC69'>		<span class="nv">ret</span><span class="o">=</span>1</div><div class='line' id='LC70'>	<span class="k">fi</span></div><div class='line' id='LC71'><span class="k">	return</span> <span class="nv">$ret</span></div><div class='line' id='LC72'><span class="o">}</span>        </div><div class='line' id='LC73'><br/></div><div class='line' id='LC74'>main_zimbashckup<span class="o">()</span> <span class="o">{</span></div><div class='line' id='LC75'>	<span class="nv">ZHOME</span><span class="o">=</span>/opt/zimbra</div><div class='line' id='LC76'>	<span class="nv">ZBACKUP</span><span class="o">=</span><span class="nv">$ZHOME</span>/backup/mailbox</div><div class='line' id='LC77'>	<span class="nv">ZCONFD</span><span class="o">=</span><span class="nv">$ZHOME</span>/conf</div><div class='line' id='LC78'>	<span class="nv">DATE</span><span class="o">=</span><span class="k">$(</span>date +%Y/%m/%d<span class="k">)</span></div><div class='line' id='LC79'>	<span class="nv">ZDUMPDIR</span><span class="o">=</span><span class="nv">$ZBACKUP</span>/<span class="nv">$DATE</span></div><div class='line' id='LC80'>	<span class="nv">ZMBOX</span><span class="o">=</span>/opt/zimbra/bin/zmmailbox</div><div class='line' id='LC81'>	<span class="k">if</span> <span class="o">[</span> -z <span class="s2">&quot;$FORMAT&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC82'><span class="k">		</span><span class="nv">FORMAT</span><span class="o">=</span><span class="s2">&quot;tar&quot;</span></div><div class='line' id='LC83'>	<span class="k">fi</span></div><div class='line' id='LC84'><span class="k">	if</span> <span class="o">[</span> -z <span class="s2">&quot;$MBOXES&quot;</span> <span class="o">]</span> <span class="o">&amp;&amp;</span> <span class="o">[</span> -z <span class="s2">&quot;$DOMAINS&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC85'><span class="k">		</span><span class="nv">MBOXES</span><span class="o">=</span><span class="k">$(</span>zmprov -l gaa<span class="k">)</span></div><div class='line' id='LC86'>	<span class="k">elif</span> <span class="o">[</span> ! -z <span class="s2">&quot;$DOMAINS&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC87'><span class="k">		</span><span class="nv">MBOXES</span><span class="o">=</span><span class="k">$(for </span>d in <span class="nv">$DOMAINS</span><span class="p">;</span> <span class="k">do </span>zmprov -l gaa <span class="nv">$d</span><span class="p">;</span><span class="k">done)</span></div><div class='line' id='LC88'>	<span class="k">fi</span></div><div class='line' id='LC89'><span class="k">	if</span> <span class="o">[</span> ! -d <span class="nv">$ZDUMPDIR</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC90'><span class="k">		</span>mkdir -p <span class="nv">$ZDUMPDIR</span></div><div class='line' id='LC91'>	<span class="k">fi</span></div><div class='line' id='LC92'><span class="k">	for </span>mbox in <span class="nv">$MBOXES</span><span class="p">;</span> <span class="k">do</span></div><div class='line' id='LC93'><span class="k">		</span><span class="nv">FOLDERS</span><span class="o">=</span><span class="s1">&#39;&#39;</span></div><div class='line' id='LC94'>		<span class="nb">test</span> -d <span class="nv">$ZDUMPDIR</span>/<span class="k">${</span><span class="nv">mbox</span><span class="k">}</span> <span class="o">||</span> mkdir -p <span class="nv">$ZDUMPDIR</span>/<span class="k">${</span><span class="nv">mbox</span><span class="k">}</span>/</div><div class='line' id='LC95'>		<span class="k">if</span> <span class="o">[</span> -z <span class="s2">&quot;$UNITE&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC96'><span class="k">			</span>echoverbose <span class="s2">&quot;\_ $mbox&quot;</span></div><div class='line' id='LC97'>			<span class="nv">FOLDERSRAW</span><span class="o">=</span><span class="k">$(</span><span class="nv">$ZMBOX</span> -z -m <span class="nv">$mbox</span> getAllFolders <span class="p">|</span> tail -n +4 <span class="p">|</span> awk <span class="s1">&#39;{ if($4 &gt; 0){$1=&quot;&quot;; $3=&quot;&quot;; $4=&quot;&quot;; print $0 } }&#39;</span> <span class="p">|</span> sed -e <span class="s2">&quot;s/  */ /g&quot;</span> <span class="p">|</span> sed -e <span class="s2">&quot;s/^ *//&quot;</span><span class="k">)</span></div><div class='line' id='LC98'>			<span class="k">if</span> <span class="o">[</span> <span class="k">$(</span><span class="nb">echo</span> <span class="nv">$FOLDERSRAW</span> <span class="p">|</span> wc -c<span class="k">)</span> -gt 1 <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC99'><span class="k">				while </span><span class="nb">read type </span>fname<span class="p">;</span> <span class="k">do</span></div><div class='line' id='LC100'>					<span class="nv">$ZMBOX</span> -z -m <span class="nv">$mbox</span> getFolder <span class="s2">&quot;$(echo $fname | sed -e &quot;</span>s/ <span class="o">(</span>.*:.*<span class="o">)</span>//<span class="s2">&quot;)&quot;</span> <span class="p">|</span> grep -q <span class="s1">&#39;ownerDisplayName&#39;</span></div><div class='line' id='LC101'>					<span class="nv">ret</span><span class="o">=</span><span class="nv">$?</span></div><div class='line' id='LC102'>					<span class="k">if</span> <span class="o">[</span> <span class="s2">&quot;$ret&quot;</span> -gt <span class="s2">&quot;0&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC103'><span class="k">						</span><span class="nv">FOLDERS</span><span class="o">=</span><span class="k">$(</span><span class="nb">echo</span> -ne <span class="s2">&quot;${FOLDERS}\n${fname}&quot;</span><span class="k">)</span></div><div class='line' id='LC104'>					<span class="k">fi</span></div><div class='line' id='LC105'><span class="k">				done</span> &lt; &lt;<span class="o">(</span><span class="nb">echo</span> <span class="s2">&quot;$FOLDERSRAW&quot;</span><span class="o">)</span></div><div class='line' id='LC106'>			<span class="k">fi</span></div><div class='line' id='LC107'><span class="k">		else</span></div><div class='line' id='LC108'><span class="k">			</span><span class="nv">FOLDERS</span><span class="o">=</span><span class="s2">&quot;/&quot;</span></div><div class='line' id='LC109'>			echoverbose <span class="s2">&quot;\_ $mbox =&gt; $ZDUMPDIR/${mbox}/full.$FORMAT&quot;</span></div><div class='line' id='LC110'>		<span class="k">fi</span></div><div class='line' id='LC111'><span class="k">		</span><span class="nb">test</span> -z <span class="s2">&quot;$FOLDERS&quot;</span> <span class="o">&amp;&amp;</span> echoverbose <span class="s1">&#39;    Nothing to backup here...&#39;</span></div><div class='line' id='LC112'>		<span class="k">while </span><span class="nb">read </span>fname<span class="p">;</span> <span class="k">do</span></div><div class='line' id='LC113'><span class="k">			if</span> <span class="o">[</span> -z <span class="s2">&quot;$UNITE&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC114'><span class="k">				</span><span class="nv">folder</span><span class="o">=</span><span class="k">$(</span><span class="nb">echo</span> <span class="nv">$fname</span> <span class="p">|</span> sed -e <span class="s2">&quot;s/::space::/ /g&quot;</span><span class="k">)</span></div><div class='line' id='LC115'>				<span class="nv">filefoldername</span><span class="o">=</span><span class="k">$(</span><span class="nb">echo</span> <span class="nv">$fname</span> <span class="p">|</span> sed -e <span class="s2">&quot;s?/?.?g&quot;</span> <span class="p">|</span> sed -e <span class="s2">&quot;s/^\.//&quot;</span><span class="k">)</span></div><div class='line' id='LC116'>				echoverbose <span class="s1">&#39;    \_ &#39;</span><span class="s2">&quot;$folder =&gt; $ZDUMPDIR/${mbox}/${filefoldername}.$FORMAT&quot;</span></div><div class='line' id='LC117'>			<span class="k">else</span></div><div class='line' id='LC118'><span class="k">				</span><span class="nv">folder</span><span class="o">=</span><span class="s2">&quot;$fname&quot;</span></div><div class='line' id='LC119'>				<span class="nv">filefoldername</span><span class="o">=</span><span class="s2">&quot;full&quot;</span></div><div class='line' id='LC120'>			<span class="k">fi</span></div><div class='line' id='LC121'>			<span class="nv">$ZMBOX</span> -t 600 -z -m <span class="nv">$mbox</span> getRestURL <span class="s2">&quot;$folder/?fmt=$FORMAT&quot;</span> &gt; <span class="s2">&quot;$ZDUMPDIR/${mbox}/${filefoldername}.$FORMAT&quot;</span></div><div class='line' id='LC122'>			<span class="nv">ret</span><span class="o">=</span><span class="nv">$?</span></div><div class='line' id='LC123'>			<span class="k">if</span> <span class="o">[</span> <span class="s2">&quot;$ret&quot;</span> -gt <span class="s2">&quot;0&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC124'><span class="k">				</span>echoerror <span class="s2">&quot;Unable to backup folder $folder, skipping&quot;</span></div><div class='line' id='LC125'>			<span class="k">fi</span></div><div class='line' id='LC126'><span class="k">			</span>sleep 1</div><div class='line' id='LC127'>		<span class="k">done</span> &lt; &lt;<span class="o">(</span><span class="nb">echo</span> <span class="s2">&quot;$FOLDERS&quot;</span>  <span class="p">|</span> grep -v <span class="s2">&quot;^$&quot;</span><span class="o">)</span></div><div class='line' id='LC128'>		zmprov ga <span class="nv">$mbox</span> zimbraMailSieveScript &gt; <span class="s2">&quot;$ZDUMPDIR/${mbox}/filters.sieve&quot;</span></div><div class='line' id='LC129'>		echoverbose <span class="s1">&#39;    \_ Mail filters (in sieve format)&#39;</span><span class="s2">&quot; =&gt; $ZDUMPDIR/${mbox}/filters.sieve&quot;</span></div><div class='line' id='LC130'>		<span class="nb">unset </span>FOLDERS FOLDERSRAW</div><div class='line' id='LC131'>	<span class="k">done</span></div><div class='line' id='LC132'><span class="k">	if</span> <span class="o">[</span> ! -z <span class="s2">&quot;$POSTSCRIPT&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC133'><span class="k">		</span><span class="nb">exec</span> <span class="nv">$POSTSCRIPT</span></div><div class='line' id='LC134'>	<span class="k">fi</span></div><div class='line' id='LC135'><span class="o">}</span></div><div class='line' id='LC136'><br/></div><div class='line' id='LC137'><span class="nb">export</span> -f main_zimbashckup</div><div class='line' id='LC138'><br/></div><div class='line' id='LC139'><span class="k">case</span> <span class="s2">&quot;$(id -nu)&quot;</span> in</div><div class='line' id='LC140'>	root<span class="o">)</span></div><div class='line' id='LC141'>		<span class="nb">echo</span> <span class="nv">$0</span> <span class="p">|</span>grep -qE <span class="s2">&quot;^/&quot;</span> <span class="o">&amp;&amp;</span> <span class="nv">progname</span><span class="o">=</span><span class="nv">$0</span> <span class="o">||</span> <span class="nv">progname</span><span class="o">=</span><span class="nv">$PWD</span>/<span class="nv">$0</span></div><div class='line' id='LC142'>		<span class="nb">set</span> -- <span class="sb">`</span>getopt -n<span class="nv">$0</span> -u --longoptions<span class="o">=</span><span class="s2">&quot;verbose unite postscript: mailboxes: domains: format: version changelog help&quot;</span> <span class="s2">&quot;vup:m:d:f:Vch&quot;</span> <span class="s2">&quot;$@&quot;</span><span class="sb">`</span></div><div class='line' id='LC143'>		<span class="nv">args</span><span class="o">=</span><span class="s2">&quot;$@&quot;</span></div><div class='line' id='LC144'>		su - zimbra --command<span class="o">=</span><span class="s2">&quot;FROMROOT=1 $progname ${args}&quot;</span></div><div class='line' id='LC145'>		<span class="p">;;</span></div><div class='line' id='LC146'>	zimbra<span class="o">)</span></div><div class='line' id='LC147'>		<span class="k">if</span> <span class="o">[</span> -z <span class="s2">&quot;$FROMROOT&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC148'><span class="k">			</span><span class="nb">set</span> -- <span class="sb">`</span>getopt -n<span class="nv">$0</span> -u --longoptions<span class="o">=</span><span class="s2">&quot;verbose unite postscript: mailboxes: domains: format: version changelog help&quot;</span> <span class="s2">&quot;vup:m:d:f:Vch&quot;</span> <span class="s2">&quot;$@&quot;</span><span class="sb">`</span></div><div class='line' id='LC149'>		<span class="k">fi</span></div><div class='line' id='LC150'><span class="k">		while</span> <span class="o">[</span> <span class="nv">$# </span>-gt 0 <span class="o">]</span><span class="p">;</span> <span class="k">do</span></div><div class='line' id='LC151'><span class="k">			case</span> <span class="s2">&quot;$1&quot;</span> in</div><div class='line' id='LC152'>				-h<span class="p">|</span>--help<span class="o">)</span></div><div class='line' id='LC153'>					usage</div><div class='line' id='LC154'>					<span class="nb">exit </span>0</div><div class='line' id='LC155'>					<span class="p">;;</span></div><div class='line' id='LC156'>				-V<span class="p">|</span>--version<span class="o">)</span></div><div class='line' id='LC157'>					version</div><div class='line' id='LC158'>					<span class="nb">exit </span>0</div><div class='line' id='LC159'>					<span class="p">;;</span></div><div class='line' id='LC160'>				-c<span class="p">|</span>--changelog<span class="o">)</span></div><div class='line' id='LC161'>					changelog</div><div class='line' id='LC162'>					<span class="nb">exit </span>0</div><div class='line' id='LC163'>					<span class="p">;;</span></div><div class='line' id='LC164'>				-v<span class="p">|</span>--verbose<span class="o">)</span></div><div class='line' id='LC165'>					<span class="nv">VERBOSE</span><span class="o">=</span><span class="s2">&quot;yes&quot;</span></div><div class='line' id='LC166'>					<span class="p">;;</span></div><div class='line' id='LC167'>				-u<span class="p">|</span>--unite<span class="o">)</span></div><div class='line' id='LC168'>					<span class="nv">UNITE</span><span class="o">=</span><span class="s2">&quot;yes&quot;</span></div><div class='line' id='LC169'>					<span class="p">;;</span></div><div class='line' id='LC170'>				-p<span class="p">|</span>--postscript<span class="o">)</span></div><div class='line' id='LC171'>					<span class="nv">POSTSCRIPT</span><span class="o">=</span><span class="s2">&quot;$2&quot;</span></div><div class='line' id='LC172'>					<span class="nb">shift</span></div><div class='line' id='LC173'>					<span class="p">;;</span></div><div class='line' id='LC174'>				-m<span class="p">|</span>--mailboxes<span class="o">)</span></div><div class='line' id='LC175'>					<span class="nv">MBOXES</span><span class="o">=</span><span class="nv">$2</span></div><div class='line' id='LC176'>					<span class="nb">shift</span></div><div class='line' id='LC177'><span class="nb">					echo</span> <span class="nv">$2</span> <span class="p">|</span> grep -vq <span class="s2">&quot;^-&quot;</span></div><div class='line' id='LC178'>					<span class="nv">v</span><span class="o">=</span><span class="nv">$?</span></div><div class='line' id='LC179'>					<span class="k">while</span> <span class="o">[</span> <span class="nv">$v</span> -eq <span class="s2">&quot;0&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">do</span></div><div class='line' id='LC180'><span class="k">						</span><span class="nv">MBOXES</span><span class="o">=</span><span class="nv">$MBOXES</span><span class="s2">&quot; &quot;</span><span class="nv">$2</span></div><div class='line' id='LC181'>						<span class="nb">shift</span></div><div class='line' id='LC182'><span class="nb">						</span><span class="k">if</span> <span class="o">[</span> <span class="s2">&quot;x&quot;</span><span class="nv">$2</span> <span class="o">==</span> <span class="s2">&quot;x&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC183'><span class="k">							</span><span class="nv">v</span><span class="o">=</span>1</div><div class='line' id='LC184'>						<span class="k">else</span></div><div class='line' id='LC185'><span class="k">							</span><span class="nb">echo</span> <span class="nv">$2</span> <span class="p">|</span> grep -vq <span class="s2">&quot;^-&quot;</span></div><div class='line' id='LC186'>							<span class="nv">v</span><span class="o">=</span><span class="nv">$?</span></div><div class='line' id='LC187'>						<span class="k">fi</span></div><div class='line' id='LC188'><span class="k">					done</span></div><div class='line' id='LC189'>					<span class="p">;;</span></div><div class='line' id='LC190'>				-d<span class="p">|</span>--domains<span class="o">)</span></div><div class='line' id='LC191'>					<span class="nv">DOMAINS</span><span class="o">=</span><span class="nv">$2</span></div><div class='line' id='LC192'>					<span class="nb">shift</span></div><div class='line' id='LC193'><span class="nb">					echo</span> <span class="nv">$2</span> <span class="p">|</span> grep -vq <span class="s2">&quot;^-&quot;</span></div><div class='line' id='LC194'>					<span class="nv">v</span><span class="o">=</span><span class="nv">$?</span></div><div class='line' id='LC195'>					<span class="k">while</span> <span class="o">[</span> <span class="nv">$v</span> -eq <span class="s2">&quot;0&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">do</span></div><div class='line' id='LC196'><span class="k">						</span><span class="nv">DOMAINS</span><span class="o">=</span><span class="nv">$DOMAINS</span><span class="s2">&quot; &quot;</span><span class="nv">$2</span></div><div class='line' id='LC197'>						<span class="nb">shift</span></div><div class='line' id='LC198'><span class="nb">						</span><span class="k">if</span> <span class="o">[</span> <span class="s2">&quot;x&quot;</span><span class="nv">$2</span> <span class="o">==</span> <span class="s2">&quot;x&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC199'><span class="k">							</span><span class="nv">v</span><span class="o">=</span>1</div><div class='line' id='LC200'>						<span class="k">else</span></div><div class='line' id='LC201'><span class="k">							</span><span class="nb">echo</span> <span class="nv">$2</span> <span class="p">|</span> grep -vq <span class="s2">&quot;^-&quot;</span></div><div class='line' id='LC202'>							<span class="nv">v</span><span class="o">=</span><span class="nv">$?</span></div><div class='line' id='LC203'>						<span class="k">fi</span></div><div class='line' id='LC204'><span class="k">					done</span></div><div class='line' id='LC205'>					<span class="p">;;</span></div><div class='line' id='LC206'>				-f<span class="p">|</span>--format<span class="o">)</span></div><div class='line' id='LC207'>					<span class="nb">echo</span> <span class="nv">$2</span> <span class="p">|</span> grep -qE <span class="s2">&quot;(tgz|tar|zip)&quot;</span></div><div class='line' id='LC208'>					<span class="nv">ret</span><span class="o">=</span><span class="nv">$?</span></div><div class='line' id='LC209'>					<span class="k">if</span> <span class="o">[</span> <span class="nv">$ret</span> -gt <span class="s2">&quot;0&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC210'><span class="k">						</span>echoerror <span class="s2">&quot;The format must be one on these three values : tar, tgz, zip.&quot;</span></div><div class='line' id='LC211'>						<span class="nb">exit </span>10</div><div class='line' id='LC212'>					<span class="k">fi</span></div><div class='line' id='LC213'>					<span class="c">#echo $2</span></div><div class='line' id='LC214'>					<span class="nv">FORMAT</span><span class="o">=</span><span class="s2">&quot;$2&quot;</span></div><div class='line' id='LC215'>					<span class="nb">shift</span></div><div class='line' id='LC216'>					<span class="p">;;</span></div><div class='line' id='LC217'>				--<span class="o">)</span></div><div class='line' id='LC218'>					<span class="nb">shift</span></div><div class='line' id='LC219'>					<span class="p">;;</span></div><div class='line' id='LC220'>			<span class="k">esac</span></div><div class='line' id='LC221'><span class="k">			</span><span class="nb">shift</span></div><div class='line' id='LC222'><span class="nb">		</span><span class="k">done</span></div><div class='line' id='LC223'><span class="k">		</span>checkrequirements</div><div class='line' id='LC224'>		<span class="k">if</span> <span class="o">[</span> <span class="nv">$?</span> -gt 0 <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC225'><span class="k">			</span>echoerror <span class="s2">&quot;Please install the missing tools and rerun this script&quot;</span></div><div class='line' id='LC226'>			<span class="nb">exit </span>11</div><div class='line' id='LC227'>		<span class="k">fi</span></div><div class='line' id='LC228'><span class="k">		if</span> <span class="o">[</span> ! -z <span class="s2">&quot;$MBOXES&quot;</span> <span class="o">]</span> <span class="o">&amp;&amp;</span> <span class="o">[</span> ! -z <span class="s2">&quot;$DOMAINS&quot;</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span></div><div class='line' id='LC229'><span class="k">			</span>echoerror <span class="s2">&quot;You can&#39;t use --mailboxes and --domains alltogether&quot;</span></div><div class='line' id='LC230'>			<span class="nb">exit </span>12</div><div class='line' id='LC231'>		<span class="k">fi</span></div><div class='line' id='LC232'><span class="k">		</span>main_zimbashckup</div><div class='line' id='LC233'>		<span class="p">;;</span></div><div class='line' id='LC234'>	*<span class="o">)</span></div><div class='line' id='LC235'>		<span class="nb">echo</span> <span class="s2">&quot;Please run this program using either the root or the zimbra user&quot;</span></div><div class='line' id='LC236'>		<span class="nb">exit </span>1</div><div class='line' id='LC237'><span class="k">esac</span></div></pre></div></td>
          </tr>
        </table>
  </div>

  </div>
</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" class="js-jump-to-line" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" class="js-jump-to-line-form">
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="button">Go</button>
  </form>
</div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer">
    <ul class="site-footer-links right">
      <li><a href="https://status.github.com/">Status</a></li>
      <li><a href="http://developer.github.com">API</a></li>
      <li><a href="http://training.github.com">Training</a></li>
      <li><a href="http://shop.github.com">Shop</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>

    </ul>

    <a href="/">
      <span class="mega-octicon octicon-mark-github" title="GitHub"></span>
    </a>

    <ul class="site-footer-links">
      <li>&copy; 2014 <span title="0.06027s from github-fe137-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="/site/terms">Terms</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
  </div><!-- /.site-footer -->
</div><!-- /.container -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-fullscreen-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="js-fullscreen-contents" placeholder="" data-suggester="fullscreen_suggester"></textarea>
          <div class="suggester-container">
              <div class="suggester fullscreen-suggester js-navigation-container" id="fullscreen_suggester"
                 data-url="/davromaniak/zimbashckup/suggestions/commit">
              </div>
          </div>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped leftwards" aria-label="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped leftwards"
      aria-label="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-remove-close close js-ajax-error-dismiss"></a>
      Something went wrong with that request. Please try again.
    </div>

  </body>
</html>

