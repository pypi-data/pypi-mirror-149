(self["webpackChunkblack_knight"] = self["webpackChunkblack_knight"] || []).push([[913],{

/***/ 71:
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

!function(t,e){ true?module.exports=e(__webpack_require__(294)):0}(self,(function(t){return(()=>{"use strict";var e={790:function(t,e,r){var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0}),e.Avatar=void 0;var a=n(r(156));e.Avatar=function(t){var e=t.picture,r=t.username;if(e)return a.default.createElement("img",{src:e,draggable:!1,alt:"".concat(r||"user"," avatar"),onContextMenu:function(t){return t.preventDefault()}});var n=i();return a.default.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",width:"100%",height:"100%",viewBox:"0 0 5 5"},a.default.createElement("rect",{x:"0",y:"0",width:"100%",height:"100%",rx:"0",fill:n.b}),a.default.createElement("text",{x:"50%",y:"50%",dy:".1em",fill:n.c,textAnchor:"middle",dominantBaseline:"middle",style:{fontFamily:"inherit",fontSize:"3px",lineHeight:1,textTransform:"uppercase",fontWeight:"bold"}},o(r)),a.default.createElement("defs",null,a.default.createElement("linearGradient",{id:"gradient",x1:"0%",y1:"0%",x2:"100%",y2:"0"},a.default.createElement("stop",{offset:"0%",stopColor:"#ff0000"}),a.default.createElement("stop",{offset:"10%",stopColor:"#ff9a00"}),a.default.createElement("stop",{offset:"20%",stopColor:"#d0de21"}),a.default.createElement("stop",{offset:"30%",stopColor:"#4fdc4a"}),a.default.createElement("stop",{offset:"40%",stopColor:"#3fdad8"}),a.default.createElement("stop",{offset:"50%",stopColor:"#2fc9e2"}),a.default.createElement("stop",{offset:"60%",stopColor:"#1c7fee"}),a.default.createElement("stop",{offset:"70%",stopColor:"#5f15f2"}),a.default.createElement("stop",{offset:"80%",stopColor:"#ba0cf8"}),a.default.createElement("stop",{offset:"90%",stopColor:"#fb07d9"}),a.default.createElement("stop",{offset:"100%",stopColor:"#ff0000"})),a.default.createElement("pattern",{id:"pattern",x:"0",y:"0",width:"300%",height:"100%",patternUnits:"userSpaceOnUse"},a.default.createElement("rect",{x:"0",y:"0",width:"150%",height:"100%",fill:"url(#gradient)"},a.default.createElement("animate",{attributeType:"XML",attributeName:"x",from:"0",to:"150%",dur:"3s",repeatCount:"indefinite"})),a.default.createElement("rect",{x:"-150%",y:"0",width:"150%",height:"100%",fill:"url(#gradient)"},a.default.createElement("animate",{attributeType:"XML",attributeName:"x",from:"-150%",to:"0",dur:"3s",repeatCount:"indefinite"})))))};var o=function(t){if(!t)return"G";try{return String.fromCodePoint(t.codePointAt(0))}catch(e){return t.charAt(0)}},i=function(){var t=Math.floor(16777215*Math.random()),e="#"+t.toString(16);if(7!==e.length)return i();var r="#fff";return.2126*(t>>16&255)+.7152*(t>>8&255)+.0722*(t>>0&255)>200&&(r="#000"),707===Math.floor(1e3*Math.random())?{b:"#040404",c:"url(#pattern)"}:{b:e,c:r}}},457:function(t,e,r){var n=this&&this.__assign||function(){return n=Object.assign||function(t){for(var e,r=1,n=arguments.length;r<n;r++)for(var a in e=arguments[r])Object.prototype.hasOwnProperty.call(e,a)&&(t[a]=e[a]);return t},n.apply(this,arguments)},a=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var o=a(r(156)),i={fill:"freeze",calcMode:"spline",keyTimes:"0; 1",keySplines:"0.35, 0.18, 0.2, 1.0"},u=function(t,e){return"OOTeamLoadingAnime".concat(t).concat(e)};e.default=function(t){var e=t.point,r=t.index,a=t.dur,l=t.points,c=l.length-1,s=r===c?l.at(0):l.at(r+1);if(!s)return o.default.createElement(o.default.Fragment,null);var f=e[0],p=e[1],d=s[0],h=s[1],m=0===r?"0;".concat(u(2,c),".end"):"".concat(u(1,r-1),".end"),v="".concat(0===r?u(1,c):u(2,r-1),".end"),y="".concat(0===r?u(2,c):u(1,r-1),".end");return o.default.createElement("line",{x1:f,y1:p,x2:f,y2:p,visibility:"hidden"},o.default.createElement("animate",{attributeName:"visibility",values:"visible",dur:"0s",begin:m,fill:"freeze"}),o.default.createElement("animate",{attributeName:"visibility",values:"hidden",dur:"0s",begin:"".concat(u(2,r),".end"),fill:"freeze"}),o.default.createElement("animate",n({id:u(1,r),attributeName:"x2",values:"".concat(f,";").concat(d),begin:m,dur:a},i)),o.default.createElement("animate",n({attributeName:"y2",values:"".concat(p,";").concat(h),begin:m,dur:a},i)),o.default.createElement("animate",n({id:u(2,r),attributeName:"x1",values:"".concat(f,";").concat(d),begin:v,dur:a},i)),o.default.createElement("animate",n({attributeName:"y1",values:"".concat(p,";").concat(h),begin:v,dur:a},i)),o.default.createElement("animate",{attributeName:"x1",values:"".concat(f),dur:"0s",begin:y}),o.default.createElement("animate",{attributeName:"y1",values:"".concat(p),dur:"0s",begin:y}))}},145:function(t,e){var r=this&&this.__assign||function(){return r=Object.assign||function(t){for(var e,r=1,n=arguments.length;r<n;r++)for(var a in e=arguments[r])Object.prototype.hasOwnProperty.call(e,a)&&(t[a]=e[a]);return t},r.apply(this,arguments)};Object.defineProperty(e,"__esModule",{value:!0}),e.GetTheShape=e.toPath=e.DataBase=void 0;var n={hexagon:{viewBox:"0 0 6 6",points:[[1.5,.4],[0,3],[1.5,5.6],[4.5,5.6],[6,3],[4.5,.4]]},triangle:{viewBox:"0 0 1 1",points:[[.5,.04],[0,.96],[1,.96]]}};e.DataBase=n;var a=function(t){return"M"+t.map((function(t){return"".concat(t[0]," ").concat(t[1])})).join(" ")};e.toPath=a,e.GetTheShape=function(t){if("string"!=typeof t)return r({path:a(t.points)},t);var e=n[t];return r({path:a(e.points)},e)}},502:function(t,e,r){var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0}),e.Loading=void 0;var a=n(r(156)),o=r(145),i=n(r(457));e.Loading=function(t){var e=t.duration,r=void 0===e?"707ms":e,n=t.shape,u=void 0===n?"hexagon":n,l=(0,o.GetTheShape)(u),c=l.path,s=l.points,f=l.viewBox;return a.default.createElement("svg",{viewBox:f},a.default.createElement("clipPath",{id:"hex"},a.default.createElement("path",{d:c})),a.default.createElement("g",{clipPath:"url(#hex)"},s.map((function(t,e){return a.default.createElement(i.default,{point:t,points:s,index:e,key:e,dur:r})}))))}},607:function(t,e,r){var n=this&&this.__createBinding||(Object.create?function(t,e,r,n){void 0===n&&(n=r);var a=Object.getOwnPropertyDescriptor(e,r);a&&!("get"in a?!e.__esModule:a.writable||a.configurable)||(a={enumerable:!0,get:function(){return e[r]}}),Object.defineProperty(t,n,a)}:function(t,e,r,n){void 0===n&&(n=r),t[n]=e[r]}),a=this&&this.__exportStar||function(t,e){for(var r in t)"default"===r||Object.prototype.hasOwnProperty.call(e,r)||n(e,t,r)};Object.defineProperty(e,"__esModule",{value:!0}),a(r(790),e),a(r(502),e),a(r(928),e)},129:function(t,e,r){var n,a=this&&this.__extends||(n=function(t,e){return n=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var r in e)Object.prototype.hasOwnProperty.call(e,r)&&(t[r]=e[r])},n(t,e)},function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Class extends value "+String(e)+" is not a constructor or null");function r(){this.constructor=t}n(t,e),t.prototype=null===e?Object.create(e):(r.prototype=e.prototype,new r)});Object.defineProperty(e,"__esModule",{value:!0}),e.CountAnim=void 0;var o=function(t){function e(){var e=null!==t&&t.apply(this,arguments)||this;return e.state={Count:e.props.start||0,accumulator:0},e.formatter=new Intl.NumberFormat,e.UpdaterID=null,e.CheckEnd=function(t,e){return e<=t},e.Operation=function(t,e){return Math.ceil(t+e)},e.UpdateCounter=e.UpdateCounterPr.bind(e),e}return a(e,t),e.prototype.ClearUpdater=function(){this.UpdaterID&&(clearInterval(this.UpdaterID),this.UpdaterID=null)},e.prototype.UpdateCounterPr=function(){var t=this;this.setState((function(e){if(!t.CheckEnd(e.Count,t.props.end)){var r=t.Operation(e.Count,e.accumulator);return t.CheckEnd(r,t.props.end)?(t.ClearUpdater(),{Count:t.props.end}):{Count:r}}return t.ClearUpdater(),null}))},e.prototype.StartUpdate=function(){this.ClearUpdater(),this.UpdaterID=setInterval(this.UpdateCounter,this.props.speed||70)},e.prototype.GetAccumulator=function(){return Math.ceil(this.props.end/77*1e5)/1e5},e.prototype.componentDidMount=function(){this.props.CheckEnd&&(this.CheckEnd=this.props.CheckEnd),this.props.Operation&&(this.Operation=this.props.Operation),this.props.GetAccumulator&&(this.GetAccumulator=this.props.GetAccumulator),this.setState({accumulator:this.GetAccumulator()}),this.StartUpdate()},e.prototype.componentDidUpdate=function(t){t.end===this.props.end&&t.start===this.props.start||("number"==typeof this.props.start&&this.setState({Count:this.props.start}),this.setState({accumulator:this.GetAccumulator()}),this.StartUpdate())},e.prototype.render=function(){return!1===this.props.format?this.state.Count.toString():this.formatter.format(this.state.Count).toString()},e}(r(156).Component);e.CountAnim=o,e.default=o},208:(t,e)=>{Object.defineProperty(e,"__esModule",{value:!0}),e.DisplayNumbers=e.Empty=e.C=void 0,e.C=function(t,e){return t?" ".concat(e," "):""},e.Empty=function(t){return 0===Object.keys(t).length};var r=Intl.NumberFormat("en",{notation:"compact"});e.DisplayNumbers=function(t,e,n){void 0===e&&(e=1e3),n||(n=10*e);var a=r.format(n);if(n.toString().length,n<e)throw Error("max cant be smaller that min");return t<=e?t.toString():t>=n?"+"+a:r.format(t)}},928:function(t,e,r){var n=this&&this.__createBinding||(Object.create?function(t,e,r,n){void 0===n&&(n=r);var a=Object.getOwnPropertyDescriptor(e,r);a&&!("get"in a?!e.__esModule:a.writable||a.configurable)||(a={enumerable:!0,get:function(){return e[r]}}),Object.defineProperty(t,n,a)}:function(t,e,r,n){void 0===n&&(n=r),t[n]=e[r]}),a=this&&this.__exportStar||function(t,e){for(var r in t)"default"===r||Object.prototype.hasOwnProperty.call(e,r)||n(e,t,r)};Object.defineProperty(e,"__esModule",{value:!0}),a(r(208),e),a(r(405),e),a(r(129),e)},405:function(t,e,r){var n=this&&this.__assign||function(){return n=Object.assign||function(t){for(var e,r=1,n=arguments.length;r<n;r++)for(var a in e=arguments[r])Object.prototype.hasOwnProperty.call(e,a)&&(t[a]=e[a]);return t},n.apply(this,arguments)},a=this&&this.__createBinding||(Object.create?function(t,e,r,n){void 0===n&&(n=r);var a=Object.getOwnPropertyDescriptor(e,r);a&&!("get"in a?!e.__esModule:a.writable||a.configurable)||(a={enumerable:!0,get:function(){return e[r]}}),Object.defineProperty(t,n,a)}:function(t,e,r,n){void 0===n&&(n=r),t[n]=e[r]}),o=this&&this.__setModuleDefault||(Object.create?function(t,e){Object.defineProperty(t,"default",{enumerable:!0,value:e})}:function(t,e){t.default=e}),i=this&&this.__importStar||function(t){if(t&&t.__esModule)return t;var e={};if(null!=t)for(var r in t)"default"!==r&&Object.prototype.hasOwnProperty.call(t,r)&&a(e,t,r);return o(e,t),e};Object.defineProperty(e,"__esModule",{value:!0}),e.NiceDoc=void 0;var u=i(r(156));e.NiceDoc=function(t){var e=t.doc,r=t.type,a=void 0===r?"div":r,o=t.attrs;return e?u.default.createElement(u.default.Fragment,null,function(t){return t.replaceAll("\r","").split("\n").map((function(t){if(t){var e=t.split("");if(e.length>0&&e.every((function(t){return" "===t})))return""}return t}))}(e).map((function(t,e){return t?(0,u.createElement)(a,n({key:e},o),t):u.default.createElement("br",{key:e})}))):u.default.createElement(u.default.Fragment,null)}},156:e=>{e.exports=t}},r={};return function t(n){var a=r[n];if(void 0!==a)return a.exports;var o=r[n]={exports:{}};return e[n].call(o.exports,o,o.exports,t),o.exports}(607)})()}));

/***/ }),

/***/ 682:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "aU": () => (/* binding */ Action),
  "lX": () => (/* binding */ createBrowserHistory),
  "q_": () => (/* binding */ createHashHistory),
  "PP": () => (/* binding */ createMemoryHistory),
  "Ep": () => (/* binding */ createPath),
  "cP": () => (/* binding */ parsePath)
});

;// CONCATENATED MODULE: ./node_modules/@babel/runtime/helpers/esm/extends.js
function _extends() {
  _extends = Object.assign || function (target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i];

      for (var key in source) {
        if (Object.prototype.hasOwnProperty.call(source, key)) {
          target[key] = source[key];
        }
      }
    }

    return target;
  };

  return _extends.apply(this, arguments);
}
;// CONCATENATED MODULE: ./node_modules/history/index.js


/**
 * Actions represent the type of change to a location value.
 *
 * @see https://github.com/remix-run/history/tree/main/docs/api-reference.md#action
 */
var Action;

(function (Action) {
  /**
   * A POP indicates a change to an arbitrary index in the history stack, such
   * as a back or forward navigation. It does not describe the direction of the
   * navigation, only that the current index changed.
   *
   * Note: This is the default action for newly created history objects.
   */
  Action["Pop"] = "POP";
  /**
   * A PUSH indicates a new entry being added to the history stack, such as when
   * a link is clicked and a new page loads. When this happens, all subsequent
   * entries in the stack are lost.
   */

  Action["Push"] = "PUSH";
  /**
   * A REPLACE indicates the entry at the current index in the history stack
   * being replaced by a new one.
   */

  Action["Replace"] = "REPLACE";
})(Action || (Action = {}));

var readOnly =  false ? 0 : function (obj) {
  return obj;
};

function warning(cond, message) {
  if (!cond) {
    // eslint-disable-next-line no-console
    if (typeof console !== 'undefined') console.warn(message);

    try {
      // Welcome to debugging history!
      //
      // This error is thrown as a convenience so you can more easily
      // find the source for a warning that appears in the console by
      // enabling "pause on exceptions" in your JavaScript debugger.
      throw new Error(message); // eslint-disable-next-line no-empty
    } catch (e) {}
  }
}

var BeforeUnloadEventType = 'beforeunload';
var HashChangeEventType = 'hashchange';
var PopStateEventType = 'popstate';
/**
 * Browser history stores the location in regular URLs. This is the standard for
 * most web apps, but it requires some configuration on the server to ensure you
 * serve the same app at multiple URLs.
 *
 * @see https://github.com/remix-run/history/tree/main/docs/api-reference.md#createbrowserhistory
 */

function createBrowserHistory(options) {
  if (options === void 0) {
    options = {};
  }

  var _options = options,
      _options$window = _options.window,
      window = _options$window === void 0 ? document.defaultView : _options$window;
  var globalHistory = window.history;

  function getIndexAndLocation() {
    var _window$location = window.location,
        pathname = _window$location.pathname,
        search = _window$location.search,
        hash = _window$location.hash;
    var state = globalHistory.state || {};
    return [state.idx, readOnly({
      pathname: pathname,
      search: search,
      hash: hash,
      state: state.usr || null,
      key: state.key || 'default'
    })];
  }

  var blockedPopTx = null;

  function handlePop() {
    if (blockedPopTx) {
      blockers.call(blockedPopTx);
      blockedPopTx = null;
    } else {
      var nextAction = Action.Pop;

      var _getIndexAndLocation = getIndexAndLocation(),
          nextIndex = _getIndexAndLocation[0],
          nextLocation = _getIndexAndLocation[1];

      if (blockers.length) {
        if (nextIndex != null) {
          var delta = index - nextIndex;

          if (delta) {
            // Revert the POP
            blockedPopTx = {
              action: nextAction,
              location: nextLocation,
              retry: function retry() {
                go(delta * -1);
              }
            };
            go(delta);
          }
        } else {
          // Trying to POP to a location with no index. We did not create
          // this location, so we can't effectively block the navigation.
           false ? 0 : void 0;
        }
      } else {
        applyTx(nextAction);
      }
    }
  }

  window.addEventListener(PopStateEventType, handlePop);
  var action = Action.Pop;

  var _getIndexAndLocation2 = getIndexAndLocation(),
      index = _getIndexAndLocation2[0],
      location = _getIndexAndLocation2[1];

  var listeners = createEvents();
  var blockers = createEvents();

  if (index == null) {
    index = 0;
    globalHistory.replaceState(_extends({}, globalHistory.state, {
      idx: index
    }), '');
  }

  function createHref(to) {
    return typeof to === 'string' ? to : createPath(to);
  } // state defaults to `null` because `window.history.state` does


  function getNextLocation(to, state) {
    if (state === void 0) {
      state = null;
    }

    return readOnly(_extends({
      pathname: location.pathname,
      hash: '',
      search: ''
    }, typeof to === 'string' ? parsePath(to) : to, {
      state: state,
      key: createKey()
    }));
  }

  function getHistoryStateAndUrl(nextLocation, index) {
    return [{
      usr: nextLocation.state,
      key: nextLocation.key,
      idx: index
    }, createHref(nextLocation)];
  }

  function allowTx(action, location, retry) {
    return !blockers.length || (blockers.call({
      action: action,
      location: location,
      retry: retry
    }), false);
  }

  function applyTx(nextAction) {
    action = nextAction;

    var _getIndexAndLocation3 = getIndexAndLocation();

    index = _getIndexAndLocation3[0];
    location = _getIndexAndLocation3[1];
    listeners.call({
      action: action,
      location: location
    });
  }

  function push(to, state) {
    var nextAction = Action.Push;
    var nextLocation = getNextLocation(to, state);

    function retry() {
      push(to, state);
    }

    if (allowTx(nextAction, nextLocation, retry)) {
      var _getHistoryStateAndUr = getHistoryStateAndUrl(nextLocation, index + 1),
          historyState = _getHistoryStateAndUr[0],
          url = _getHistoryStateAndUr[1]; // TODO: Support forced reloading
      // try...catch because iOS limits us to 100 pushState calls :/


      try {
        globalHistory.pushState(historyState, '', url);
      } catch (error) {
        // They are going to lose state here, but there is no real
        // way to warn them about it since the page will refresh...
        window.location.assign(url);
      }

      applyTx(nextAction);
    }
  }

  function replace(to, state) {
    var nextAction = Action.Replace;
    var nextLocation = getNextLocation(to, state);

    function retry() {
      replace(to, state);
    }

    if (allowTx(nextAction, nextLocation, retry)) {
      var _getHistoryStateAndUr2 = getHistoryStateAndUrl(nextLocation, index),
          historyState = _getHistoryStateAndUr2[0],
          url = _getHistoryStateAndUr2[1]; // TODO: Support forced reloading


      globalHistory.replaceState(historyState, '', url);
      applyTx(nextAction);
    }
  }

  function go(delta) {
    globalHistory.go(delta);
  }

  var history = {
    get action() {
      return action;
    },

    get location() {
      return location;
    },

    createHref: createHref,
    push: push,
    replace: replace,
    go: go,
    back: function back() {
      go(-1);
    },
    forward: function forward() {
      go(1);
    },
    listen: function listen(listener) {
      return listeners.push(listener);
    },
    block: function block(blocker) {
      var unblock = blockers.push(blocker);

      if (blockers.length === 1) {
        window.addEventListener(BeforeUnloadEventType, promptBeforeUnload);
      }

      return function () {
        unblock(); // Remove the beforeunload listener so the document may
        // still be salvageable in the pagehide event.
        // See https://html.spec.whatwg.org/#unloading-documents

        if (!blockers.length) {
          window.removeEventListener(BeforeUnloadEventType, promptBeforeUnload);
        }
      };
    }
  };
  return history;
}
/**
 * Hash history stores the location in window.location.hash. This makes it ideal
 * for situations where you don't want to send the location to the server for
 * some reason, either because you do cannot configure it or the URL space is
 * reserved for something else.
 *
 * @see https://github.com/remix-run/history/tree/main/docs/api-reference.md#createhashhistory
 */

function createHashHistory(options) {
  if (options === void 0) {
    options = {};
  }

  var _options2 = options,
      _options2$window = _options2.window,
      window = _options2$window === void 0 ? document.defaultView : _options2$window;
  var globalHistory = window.history;

  function getIndexAndLocation() {
    var _parsePath = parsePath(window.location.hash.substr(1)),
        _parsePath$pathname = _parsePath.pathname,
        pathname = _parsePath$pathname === void 0 ? '/' : _parsePath$pathname,
        _parsePath$search = _parsePath.search,
        search = _parsePath$search === void 0 ? '' : _parsePath$search,
        _parsePath$hash = _parsePath.hash,
        hash = _parsePath$hash === void 0 ? '' : _parsePath$hash;

    var state = globalHistory.state || {};
    return [state.idx, readOnly({
      pathname: pathname,
      search: search,
      hash: hash,
      state: state.usr || null,
      key: state.key || 'default'
    })];
  }

  var blockedPopTx = null;

  function handlePop() {
    if (blockedPopTx) {
      blockers.call(blockedPopTx);
      blockedPopTx = null;
    } else {
      var nextAction = Action.Pop;

      var _getIndexAndLocation4 = getIndexAndLocation(),
          nextIndex = _getIndexAndLocation4[0],
          nextLocation = _getIndexAndLocation4[1];

      if (blockers.length) {
        if (nextIndex != null) {
          var delta = index - nextIndex;

          if (delta) {
            // Revert the POP
            blockedPopTx = {
              action: nextAction,
              location: nextLocation,
              retry: function retry() {
                go(delta * -1);
              }
            };
            go(delta);
          }
        } else {
          // Trying to POP to a location with no index. We did not create
          // this location, so we can't effectively block the navigation.
           false ? 0 : void 0;
        }
      } else {
        applyTx(nextAction);
      }
    }
  }

  window.addEventListener(PopStateEventType, handlePop); // popstate does not fire on hashchange in IE 11 and old (trident) Edge
  // https://developer.mozilla.org/de/docs/Web/API/Window/popstate_event

  window.addEventListener(HashChangeEventType, function () {
    var _getIndexAndLocation5 = getIndexAndLocation(),
        nextLocation = _getIndexAndLocation5[1]; // Ignore extraneous hashchange events.


    if (createPath(nextLocation) !== createPath(location)) {
      handlePop();
    }
  });
  var action = Action.Pop;

  var _getIndexAndLocation6 = getIndexAndLocation(),
      index = _getIndexAndLocation6[0],
      location = _getIndexAndLocation6[1];

  var listeners = createEvents();
  var blockers = createEvents();

  if (index == null) {
    index = 0;
    globalHistory.replaceState(_extends({}, globalHistory.state, {
      idx: index
    }), '');
  }

  function getBaseHref() {
    var base = document.querySelector('base');
    var href = '';

    if (base && base.getAttribute('href')) {
      var url = window.location.href;
      var hashIndex = url.indexOf('#');
      href = hashIndex === -1 ? url : url.slice(0, hashIndex);
    }

    return href;
  }

  function createHref(to) {
    return getBaseHref() + '#' + (typeof to === 'string' ? to : createPath(to));
  }

  function getNextLocation(to, state) {
    if (state === void 0) {
      state = null;
    }

    return readOnly(_extends({
      pathname: location.pathname,
      hash: '',
      search: ''
    }, typeof to === 'string' ? parsePath(to) : to, {
      state: state,
      key: createKey()
    }));
  }

  function getHistoryStateAndUrl(nextLocation, index) {
    return [{
      usr: nextLocation.state,
      key: nextLocation.key,
      idx: index
    }, createHref(nextLocation)];
  }

  function allowTx(action, location, retry) {
    return !blockers.length || (blockers.call({
      action: action,
      location: location,
      retry: retry
    }), false);
  }

  function applyTx(nextAction) {
    action = nextAction;

    var _getIndexAndLocation7 = getIndexAndLocation();

    index = _getIndexAndLocation7[0];
    location = _getIndexAndLocation7[1];
    listeners.call({
      action: action,
      location: location
    });
  }

  function push(to, state) {
    var nextAction = Action.Push;
    var nextLocation = getNextLocation(to, state);

    function retry() {
      push(to, state);
    }

     false ? 0 : void 0;

    if (allowTx(nextAction, nextLocation, retry)) {
      var _getHistoryStateAndUr3 = getHistoryStateAndUrl(nextLocation, index + 1),
          historyState = _getHistoryStateAndUr3[0],
          url = _getHistoryStateAndUr3[1]; // TODO: Support forced reloading
      // try...catch because iOS limits us to 100 pushState calls :/


      try {
        globalHistory.pushState(historyState, '', url);
      } catch (error) {
        // They are going to lose state here, but there is no real
        // way to warn them about it since the page will refresh...
        window.location.assign(url);
      }

      applyTx(nextAction);
    }
  }

  function replace(to, state) {
    var nextAction = Action.Replace;
    var nextLocation = getNextLocation(to, state);

    function retry() {
      replace(to, state);
    }

     false ? 0 : void 0;

    if (allowTx(nextAction, nextLocation, retry)) {
      var _getHistoryStateAndUr4 = getHistoryStateAndUrl(nextLocation, index),
          historyState = _getHistoryStateAndUr4[0],
          url = _getHistoryStateAndUr4[1]; // TODO: Support forced reloading


      globalHistory.replaceState(historyState, '', url);
      applyTx(nextAction);
    }
  }

  function go(delta) {
    globalHistory.go(delta);
  }

  var history = {
    get action() {
      return action;
    },

    get location() {
      return location;
    },

    createHref: createHref,
    push: push,
    replace: replace,
    go: go,
    back: function back() {
      go(-1);
    },
    forward: function forward() {
      go(1);
    },
    listen: function listen(listener) {
      return listeners.push(listener);
    },
    block: function block(blocker) {
      var unblock = blockers.push(blocker);

      if (blockers.length === 1) {
        window.addEventListener(BeforeUnloadEventType, promptBeforeUnload);
      }

      return function () {
        unblock(); // Remove the beforeunload listener so the document may
        // still be salvageable in the pagehide event.
        // See https://html.spec.whatwg.org/#unloading-documents

        if (!blockers.length) {
          window.removeEventListener(BeforeUnloadEventType, promptBeforeUnload);
        }
      };
    }
  };
  return history;
}
/**
 * Memory history stores the current location in memory. It is designed for use
 * in stateful non-browser environments like tests and React Native.
 *
 * @see https://github.com/remix-run/history/tree/main/docs/api-reference.md#creatememoryhistory
 */

function createMemoryHistory(options) {
  if (options === void 0) {
    options = {};
  }

  var _options3 = options,
      _options3$initialEntr = _options3.initialEntries,
      initialEntries = _options3$initialEntr === void 0 ? ['/'] : _options3$initialEntr,
      initialIndex = _options3.initialIndex;
  var entries = initialEntries.map(function (entry) {
    var location = readOnly(_extends({
      pathname: '/',
      search: '',
      hash: '',
      state: null,
      key: createKey()
    }, typeof entry === 'string' ? parsePath(entry) : entry));
     false ? 0 : void 0;
    return location;
  });
  var index = clamp(initialIndex == null ? entries.length - 1 : initialIndex, 0, entries.length - 1);
  var action = Action.Pop;
  var location = entries[index];
  var listeners = createEvents();
  var blockers = createEvents();

  function createHref(to) {
    return typeof to === 'string' ? to : createPath(to);
  }

  function getNextLocation(to, state) {
    if (state === void 0) {
      state = null;
    }

    return readOnly(_extends({
      pathname: location.pathname,
      search: '',
      hash: ''
    }, typeof to === 'string' ? parsePath(to) : to, {
      state: state,
      key: createKey()
    }));
  }

  function allowTx(action, location, retry) {
    return !blockers.length || (blockers.call({
      action: action,
      location: location,
      retry: retry
    }), false);
  }

  function applyTx(nextAction, nextLocation) {
    action = nextAction;
    location = nextLocation;
    listeners.call({
      action: action,
      location: location
    });
  }

  function push(to, state) {
    var nextAction = Action.Push;
    var nextLocation = getNextLocation(to, state);

    function retry() {
      push(to, state);
    }

     false ? 0 : void 0;

    if (allowTx(nextAction, nextLocation, retry)) {
      index += 1;
      entries.splice(index, entries.length, nextLocation);
      applyTx(nextAction, nextLocation);
    }
  }

  function replace(to, state) {
    var nextAction = Action.Replace;
    var nextLocation = getNextLocation(to, state);

    function retry() {
      replace(to, state);
    }

     false ? 0 : void 0;

    if (allowTx(nextAction, nextLocation, retry)) {
      entries[index] = nextLocation;
      applyTx(nextAction, nextLocation);
    }
  }

  function go(delta) {
    var nextIndex = clamp(index + delta, 0, entries.length - 1);
    var nextAction = Action.Pop;
    var nextLocation = entries[nextIndex];

    function retry() {
      go(delta);
    }

    if (allowTx(nextAction, nextLocation, retry)) {
      index = nextIndex;
      applyTx(nextAction, nextLocation);
    }
  }

  var history = {
    get index() {
      return index;
    },

    get action() {
      return action;
    },

    get location() {
      return location;
    },

    createHref: createHref,
    push: push,
    replace: replace,
    go: go,
    back: function back() {
      go(-1);
    },
    forward: function forward() {
      go(1);
    },
    listen: function listen(listener) {
      return listeners.push(listener);
    },
    block: function block(blocker) {
      return blockers.push(blocker);
    }
  };
  return history;
} ////////////////////////////////////////////////////////////////////////////////
// UTILS
////////////////////////////////////////////////////////////////////////////////

function clamp(n, lowerBound, upperBound) {
  return Math.min(Math.max(n, lowerBound), upperBound);
}

function promptBeforeUnload(event) {
  // Cancel the event.
  event.preventDefault(); // Chrome (and legacy IE) requires returnValue to be set.

  event.returnValue = '';
}

function createEvents() {
  var handlers = [];
  return {
    get length() {
      return handlers.length;
    },

    push: function push(fn) {
      handlers.push(fn);
      return function () {
        handlers = handlers.filter(function (handler) {
          return handler !== fn;
        });
      };
    },
    call: function call(arg) {
      handlers.forEach(function (fn) {
        return fn && fn(arg);
      });
    }
  };
}

function createKey() {
  return Math.random().toString(36).substr(2, 8);
}
/**
 * Creates a string URL path from the given pathname, search, and hash components.
 *
 * @see https://github.com/remix-run/history/tree/main/docs/api-reference.md#createpath
 */


function createPath(_ref) {
  var _ref$pathname = _ref.pathname,
      pathname = _ref$pathname === void 0 ? '/' : _ref$pathname,
      _ref$search = _ref.search,
      search = _ref$search === void 0 ? '' : _ref$search,
      _ref$hash = _ref.hash,
      hash = _ref$hash === void 0 ? '' : _ref$hash;
  if (search && search !== '?') pathname += search.charAt(0) === '?' ? search : '?' + search;
  if (hash && hash !== '#') pathname += hash.charAt(0) === '#' ? hash : '#' + hash;
  return pathname;
}
/**
 * Parses a string URL path into its separate pathname, search, and hash components.
 *
 * @see https://github.com/remix-run/history/tree/main/docs/api-reference.md#parsepath
 */

function parsePath(path) {
  var parsedPath = {};

  if (path) {
    var hashIndex = path.indexOf('#');

    if (hashIndex >= 0) {
      parsedPath.hash = path.substr(hashIndex);
      path = path.substr(0, hashIndex);
    }

    var searchIndex = path.indexOf('?');

    if (searchIndex >= 0) {
      parsedPath.search = path.substr(searchIndex);
      path = path.substr(0, searchIndex);
    }

    if (path) {
      parsedPath.pathname = path;
    }
  }

  return parsedPath;
}


//# sourceMappingURL=index.js.map


/***/ })

}]);
//# sourceMappingURL=source_maps/shared-7d5d5420.1fc8e13e1682bf957d52.js.map