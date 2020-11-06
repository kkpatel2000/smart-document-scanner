Vue.component('ctable', {
    data: function () {
        return {
            // title: 'Test',
            count: 0,
            isEdit: false,
            // thArray: ['name', 'lol', 'haha'],
            // trArray: [['sameep', '1999/11/27', '123'], ['aameep', '1999/12/27', '423'], ['ameep', '1999/11/26', '723']],
            showTable: true,
            index: -1,
            isAscending: true,
            isNewCol: false,
            newColumnName: ''
        }
    },
    props: ['title', 'thArray', 'trArray', 'isPrint'],
    template:
        `
<table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth" v-show="showTable">
<thead>
<tr>
    <th :colspan="thArray.length">
        {{ title }}
        <span class="is-pulled-right" >
            <span class="tag is-primary" @click="fixEmptyColumn()" style="cursor: pointer;" v-show="!isPrint">Fix</span>
            <span class="tag is-warning" @click="isEdit = !isEdit" style="cursor: pointer;" v-bind:class="{ 'is-light': isEdit }" v-show="!isPrint">{{ isEdit ? 'Edit Mode...' : 'Edit' }}</span>
            <span class="tag is-info ">No of Documents : {{ trArray.length }}</span>
        </span>
    </th>
</tr>
<tr>
    <th v-for="(th, index) in thArray">
        {{ th }}
        <button class="button is-small is-white is-pulled-right" @click="onThClick(index)" v-show="!isPrint">
            <span class="icon is-small">
                <span class="material-icons" v-show="isShow(index, 'up')">
                    keyboard_arrow_down
                </span>
                <span class="material-icons" v-show="isShow(index, 'down')">
                    keyboard_arrow_up
                </span>
                <span class="material-icons"  v-show="isShow(index, 'none')">
                    unfold_less
                </span>
            </span>
        </button>
    </th>
</tr>
</thead>
<tbody>
<tr v-for="(tr, row) in trArray">
    <td v-for="(td, col) in tr" @click="clickOn(row, col)" v-show="!isEdit">{{ td }}</td>
    <td v-for="(td, col) in tr" @click="clickOn(row, col)" v-show="isEdit">
        <input class="input is-small" v-model="trArray[row][col]" :placeholder="td">
    </td>
</tr>
<tr v-show="isEdit" >
    <td :colspan="thArray.length">
        <div class="buttons" >
            <button class="button is-small is-warning is-rounded" @click="addNewRow()">
                <span class="icon material-icons">
                    playlist_add
                </span>
                <span><strong>Add Row</strong></span>
            </button>
            <button class="button is-small is-warning is-rounded" @click="isNewCol = !isNewCol">
                <span class="icon material-icons" style="transform: rotate(-90deg);">
                    playlist_add
                </span>
                <span><strong>Add Column</strong></span>
            </button>
        </div>
    </td>
</tr>

</tbody>
<div class="modal" v-bind:class="{ 'is-active': isNewCol }">
    <div class="modal-background"></div>
    <div class="modal-content">
        <div class="card">
            <div class="card-content">
                <div class="content">
                    Enter New Column Name :
                    <input class="input" v-on:keyup.enter="addNewColumn" v-model="newColumnName">
                </div>
            </div>
        </div>
    </div>
    <button class="modal-close is-large" aria-label="close" @click="isNewCol = !isNewCol"></button>
</div>
</table>
`,
    methods: {
        sortIthCol: function (i) {
            var context = this
            this.trArray.sort(
                function (a, b) {
                    if (context.isAscending) {
                        return a[i].localeCompare(b[i]);
                    }
                    else {
                        return b[i].localeCompare(a[i]);
                    }
                }
            )
        },
        isShow: function (index, type) {
            if (index != this.index && type == 'none') {
                return true;
            } else if (index == this.index && type == 'down' && this.isAscending == true) {
                return true;
            } else if (index == this.index && type == 'up' && this.isAscending == false) {
                return true;
            } else {
                return false;
            }
        },
        onThClick: function (index) {
            // this.index = index
            // console.log('hi', this.index, index)
            if (this.index === index) {
                this.isAscending = !this.isAscending;
                this.sortIthCol(index);
            } else {
                this.index = index;
                this.isAscending = true;
                this.sortIthCol(index);
            }
        },
        clickOn: function (row, col) {
            console.log(row, col);
        },
        addNewColumn: function () {
            // console.log('Enter', this.newColumnName);
            this.isNewCol = false;
            // console.log(this.thArray);
            this.thArray.push(this.newColumnName);
            for (i in this.trArray) {
                this.trArray[i].push('');
            }
        },
        addNewRow: function () {
            // this.trArray.push([]);
            var newRow = [];
            for (i in this.thArray) {
                newRow.push('');
            }
            this.trArray.push(newRow);
        },
        fixEmptyColumn: function () {
            var thArrayLength = this.thArray.length;
            for (i in this.trArray) {
                while ((this.trArray[i].length < thArrayLength)) {
                    this.trArray[i].push('');
                }
            }
        }
    }
});