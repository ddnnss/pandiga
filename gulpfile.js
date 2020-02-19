var gulp = require('gulp');
    sass        = require('gulp-sass');
    browserSync = require('browser-sync');
    autoprefixer = require('gulp-autoprefixer');
    mq = require('gulp-group-css-media-queries');
    image = require('gulp-image');
gulp.task('sass', function(){
    return gulp.src('static/sass/**/*.sass')
        .pipe(sass())
        .pipe(autoprefixer({
            browsers: ['last 4 versions']
        }))
        .pipe(mq())
        .pipe(gulp.dest('static/css'))
        .pipe(browserSync.reload({stream: true}))
});

gulp.task('browser-sync', function() {
    browserSync({
        browser: 'chrome',
        server: {
            baseDir: 'static'
        },
        notify: false
    });
})

gulp.task('image', function () {
  gulp.src(['static/img/*','static/img/icons/*'])
    .pipe(image())
    .pipe(gulp.dest('static/img'));
});

gulp.task('scripts', function() {
    return gulp.src(['static/js/main.js', 'static/libs/**/*.js'])
    .pipe(browserSync.reload({ stream: true }))
});

gulp.task('code', function() {
    return gulp.src('static/*.html')
    .pipe(browserSync.reload({ stream: true }))
});

gulp.task('watch', function() {
    gulp.watch('static/sass/**/*.sass', gulp.parallel('sass'));
    gulp.watch('html/*.html', gulp.parallel('code'));
    gulp.watch(['static/js/main.js', 'html/libs/**/*.js'], gulp.parallel('scripts'));
});

gulp.task('default', gulp.parallel('sass','image', 'browser-sync', 'watch'));

