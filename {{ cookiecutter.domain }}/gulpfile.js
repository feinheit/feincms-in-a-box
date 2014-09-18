// Gulp
var gulp = require('gulp');
var base = './naturnetz/static/naturnetz/';

// Plugins
var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
var prefixer = require('gulp-autoprefixer');
var minifycss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');

// JS hint task
gulp.task('jshint', function() {
  gulp.src(base + 'js/*.js')
    .pipe(jshint())
    .pipe(jshint.reporter('default'))
    .pipe(jshint.reporter('fail'));
});

// Sass
gulp.task('sass', function() {
  gulp.src([
    base + 'scss/app.scss',
    base + 'bower_components/lightbox2/css/lightbox.css'
  ])
    .pipe(sass({
      includePaths: [base + 'bower_components/foundation/scss/.'],
      sourceComments: 'map',
      sourceMap: 'sass'
    }))
    .pipe(prefixer(
      '> 1%', 'last 2 versions', 'Firefox ESR', 'Opera 12.1'
    ))
    .pipe(concat('app.css'))
    .pipe(minifycss())
    .pipe(gulp.dest(base + 'build/'));
});

// Uglify
gulp.task('uglify', function() {
  gulp.src([
    base + 'js/*.js',
    base + 'bower_components/lightbox2/js/lightbox.js'
  ])
    .pipe(uglify())
    .pipe(concat('app.js'))
    .pipe(gulp.dest(base + 'build/'));
});


// Watch
gulp.task('watch', function(event) {
  gulp.watch(base + 'scss/*.scss', ['sass']);
  gulp.watch(base + 'js/*.js', ['uglify']);
});

// Build
gulp.task('build', ['sass', 'uglify']);

gulp.task('default', ['watch']);
