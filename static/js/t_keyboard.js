$(document).ready(function () {
    // Табы
    $('body').on('click', '.js-tab-open', function (e) {
        e.preventDefault();

        var $this = $(this),
            href = $this.attr('href');

        $(href).addClass('active').siblings().removeClass('active');

    });

    // Изменить язык
    $('body').on('mousedown', '.js-change-language', function (e) {
        e.preventDefault();

        var $this = $(this),
            $keyboard = $this.closest('.keyboard');

        if ($keyboard.hasClass('lang-ru')) {
            $keyboard.removeClass('lang-ru').addClass('lang-en');
        } else {
            $keyboard.removeClass('lang-en').addClass('lang-ru');
        }

    });

    $('body').on('mousedown', '.js-btn-caps', function (e) {
        e.preventDefault();

        var $this = $(this),
            $keyboard = $this.closest('.keyboard');

        if (!$keyboard.hasClass('uppercase')) {
            $keyboard.addClass('uppercase');
        } else {
            $keyboard.removeClass('uppercase');
        }

    });

    $('body').on('mousedown', '.js-btn-letter', function (e) {
        e.preventDefault();

        var $this = $(this),
            $keyboard = $this.closest('.keyboard'),
            $form = $($keyboard.data('form')),
            current_value = $form.find('.form-control:focus').val(),
            value;

        if ($keyboard.hasClass('lang-ru')) {
            value = $this.find('.ru').html();
        } else {
            value = $this.find('.en').html();
        }

        if ($keyboard.hasClass('uppercase')) {
            value = value.toUpperCase();
        }
        if (value == 'space') {
            value = ' ';
        }

        $form.find('.form-control:focus').val(current_value + value);
        $form.find('.form-control:focus').change();

    });

    $('body').on('mousedown', '.js-btn-backspace', function (e) {
        e.preventDefault();

        var $this = $(this),
            $keyboard = $this.closest('.keyboard'),
            $form = $($keyboard.data('form')),
            current_value = $form.find('.form-control:focus').val();

        $form.find('.form-control:focus').val(current_value.slice(0, -1));
        $form.find('.form-control:focus').change();

    });

    $('body').on('mousedown', '.js-btn-enter', function (e) {
        e.preventDefault();

        var $this = $(this),
            $keyboard = $this.closest('.keyboard'),
            $form = $($keyboard.data('form'));

        $form.find('form').submit();

    });

    $('body').on('mousedown', '.js-btn-tab', function (e) {
        e.preventDefault();

        var $this = $(this),
            $keyboard = $this.closest('.keyboard'),
            $form = $($keyboard.data('form')),
            current_value = $form.find('.form-control:focus').val();

        $form.find('.form-control:focus').val(current_value + ' ');

    });

});

TEMPLATE_KEYBOARD = `                    
                    <div class="keyboard lang-ru" id="keyboard" data-form="{data}">
                        <div class="row">
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">ё</span>
                                    <span class="en">\`</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">1</span>
                                    <span class="en">1</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">2</span>
                                    <span class="en">2</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">3</span>
                                    <span class="en">3</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">4</span>
                                    <span class="en">4</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">5</span>
                                    <span class="en">5</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">6</span>
                                    <span class="en">6</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">7</span>
                                    <span class="en">7</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">8</span>
                                    <span class="en">8</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">9</span>
                                    <span class="en">9</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">0</span>
                                    <span class="en">0</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">-</span>
                                    <span class="en">-</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">=</span>
                                    <span class="en">=</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn js-btn-backspace">backspace</button>
                            </div>
                            <div class="w-100"></div>
                            <div class="col">
                                <button class="btn js-btn-letter">
                                    <span class="ru">@</span>
                                    <span class="en">@</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">й</span>
                                    <span class="en">q</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">ц</span>
                                    <span class="en">w</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">у</span>
                                    <span class="en">e</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">к</span>
                                    <span class="en">r</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">е</span>
                                    <span class="en">t</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">н</span>
                                    <span class="en">y</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">г</span>
                                    <span class="en">u</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">ш</span>
                                    <span class="en">i</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">щ</span>
                                    <span class="en">o</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">з</span>
                                    <span class="en">p</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">х</span>
                                    <span class="en">[</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">ъ</span>
                                    <span class="en">]</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">space</span>
                                    <span class="en">space</span>
                                </button>
                            </div>
                            <div class="w-100"></div>
                            <div class="col">
                                <button class="btn js-btn-caps">caps</button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">ф</span>
                                    <span class="en">a</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">ы</span>
                                    <span class="en">s</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">в</span>
                                    <span class="en">d</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">а</span>
                                    <span class="en">f</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">п</span>
                                    <span class="en">g</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">р</span>
                                    <span class="en">h</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">о</span>
                                    <span class="en">j</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">л</span>
                                    <span class="en">k</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">д</span>
                                    <span class="en">l</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">ж</span>
                                    <span class="en">;</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">э</span>
                                    <span class="en">'</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn js-btn-enter">
                                    < enter
                                </button> 
                            </div>
                            <div class="w-100"></div>
                            <!-- <div class="col">
                                <button class="btn js-btn-shift">shift</button>
                            </div> -->
                            <div class="col">
                                <button class="btn js-change-language">
                                    <span class="icon-language"></span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">я</span>
                                    <span class="en">z</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">ч</span>
                                    <span class="en">x</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">с</span>
                                    <span class="en">c</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">м</span>
                                    <span class="en">v</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">и</span>
                                    <span class="en">b</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">т</span>
                                    <span class="en">n</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">ь</span>
                                    <span class="en">m</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">б</span>
                                    <span class="en">,</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">ю</span>
                                    <span class="en">.</span>
                                </button>
                            </div>
                            <div class="col">
                                <button class="btn btn-letter js-btn-letter">
                                    <span class="ru">.</span>
                                    <span class="en">/</span>
                                </button>
                            </div>
                            <!-- <div class="col">
                                <button class="btn js-btn-shift">shift</button>
                            </div> -->
                        </div>
                    </div>
                <!-- Клавиатура -->
`

function open_keyboard(popid,divid){
    var tmp_data = {'data':'#'+popid};
    const tmpl = render_template(TEMPLATE_KEYBOARD,tmp_data,[]);
    $('#'+divid).html(tmpl);
    $.fancybox.open({src:"#"+popid});
    
}

