// Gulp
var gulp = require('gulp');
var base = './${PROJECT_NAME}/static/${PROJECT_NAME}/';

// Plugins
var sass = require('gulp-sass');
var prefixer = require('gulp-autoprefixer');
var minifycss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');

// Sass
gulp.task('css', function() {
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
gulp.task('js', function() {
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
  gulp.watch(base + 'scss/*.scss', ['css']);
  gulp.watch(base + 'js/*.js', ['js']);
});

// Build
gulp.task('build', ['css', 'js']);
gulp.task('default', ['build', 'watch']);
