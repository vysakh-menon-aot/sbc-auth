<template>
  <v-container class="view-container pt-0">

    <!-- Breadcrumbs / Back Navigation -->
    <nav class="crumbs">
      <div class="pt-5 pb-3">
        <v-btn large text color="primary" class="back-btn pr-2 pl-1" @click="goBack()">
          <v-icon small class="mr-1">mdi-arrow-left</v-icon>
          <span>Back to Staff Dashboard</span>
        </v-btn>
      </div>
    </nav>

    <div class="view-header flex-column">
      <h1 class="view-header__title">Review Account</h1>
      <p class="mt-2 mb-0">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
    </div>
    <v-card class="mt-8" flat v-if="!isLoading">
      <v-row class="mr-0 ml-0">

        <!-- Account Information Column -->
        <v-col class="main-col col-12 col-md-8 pa-6 pa-md-8">

            <!-- Affidavit Section -->
            <section>
              <h2 class="mb-7">1. Download Affidavit</h2>
              <p class="mb-9">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at porttitor sem. Aliquam erat volutpat.</p>
              <v-btn x-large="" outlined color="primary" class="font-weight-bold" @click="downloadAffidavit()">
                <v-icon left class="mr-2">mdi-file-download-outline</v-icon>
                {{ accountUnderReview.name + '-affidavit'}}
              </v-btn>
            </section>

            <v-divider class="mt-10 mb-8"></v-divider>

            <!-- Account Info Section -->
            <section>
              <h2 class="mb-3">2. Account Information</h2>
              <v-row>
                <v-col class="col-12 col-sm-3">
                  <span v-if="accountUnderReview.orgType === 'PREMIUM'">Account Name <br/> &amp; BC Online Details</span>
                  <span v-else>Account Name</span>
                </v-col>
                <v-col>
                  <v-alert dark color="primary" class="bcol-acc mb-0 px-7 py-5">
                    <div class="bcol-acc__name mt-n1">
                      {{ accountUnderReview.name }}
                    </div>
                    <ul class="bcol-acc__meta" v-if="accountUnderReview.bcolAccountDetails">
                      <li>
                        Account No: {{ accountUnderReview.bcolAccountDetails.accountNumber }}
                      </li>
                      <li>
                        Prime Contact ID: {{ accountUnderReview.bcolAccountDetails.userId }}
                      </li>
                    </ul>
                  </v-alert>
                </v-col>
              </v-row>
              <v-row v-if="accountUnderReviewAddress">
                <v-col class="col-12 col-sm-3">
                  Mailing Address
                </v-col>
                <v-col>
                  <ul class="mailing-address">
                    <li>{{ accountUnderReviewAddress.street }}</li>
                    <li>{{ accountUnderReviewAddress.city }} {{ accountUnderReviewAddress.region }} {{ accountUnderReviewAddress.postalCode }}</li>
                    <li>{{ accountUnderReviewAddress.country }}</li>
                  </ul>
                </v-col>
              </v-row>
            </section>

            <v-divider class="mt-5 mb-8"></v-divider>

            <!-- Account Administrator Section -->
            <section v-if="accountUnderReviewAdmin">
              <h2 class="mb-5">3. Account Administrator</h2>
              <v-row>
                <v-col class="cols-12 col-sm-3 py-2">Given Name(s)</v-col>
                <v-col class="py-2">{{ accountUnderReviewAdmin.firstname }} {{ accountUnderReviewAdmin.lastname }}</v-col>
              </v-row>
              <v-row>
                <v-col class="cols-12 col-sm-3 py-2">Username</v-col>
                <v-col class="py-2">{{ accountUnderReviewAdmin.username }}</v-col>
              </v-row>
              <v-row>
                <v-col class="cols-12 col-sm-3 py-2">Email Address</v-col>
                <v-col class="py-2">{{ accountUnderReviewAdminContact.email }}</v-col>
              </v-row>
              <v-row>
                <v-col class="cols-12 col-sm-3 py-2">Phone Number</v-col>
                <v-col class="py-2">{{ accountUnderReviewAdminContact.phone }}</v-col>
              </v-row>
            </section>

            <v-divider class="mt-7 mb-8"></v-divider>

            <!-- Notary Information Section -->
            <section>
              <h2 class="mb-5">4. Notary Information</h2>
              <v-row>
                  <v-col class="cols-12 col-sm-3 py-2">Notary Name</v-col>
                  <v-col class="py-2">{{ accountNotaryName }}</v-col>
                </v-row>
                <v-row v-if="accountNotaryContact">
                  <v-col class="cols-12 col-sm-3 py-2">Mailing Address</v-col>
                  <v-col class="py-2">
                    <div>
                      <ul class="mailing-address">
                        <li>{{ accountNotaryContact.street }}</li>
                        <li>{{ accountNotaryContact.city }} {{ accountNotaryContact.region }} {{ accountNotaryContact.postalCode }}</li>
                        <li>{{ accountNotaryContact.country }}</li>
                      </ul>
                    </div>
                    </v-col>
                </v-row>
                <v-row>
                  <v-col class="cols-12 col-sm-3 py-2">Email Address</v-col>
                  <v-col class="py-2">{{ accountNotaryContact.email }}</v-col>
                </v-row>
                <v-row>
                  <v-col class="cols-12 col-sm-3 py-2">Phone Number</v-col>
                  <v-col class="py-2">{{ accountNotaryContact.phone }}</v-col>
                </v-row>
            </section>

            <v-divider class="mt-8 mb-6"></v-divider>

            <v-row class="form__btns">
              <v-col class="pb-0">
                <v-btn large :outlined="!approveSelected" color="success" class="font-weight-bold mr-2 select-button" @click="selectApprove()">
                  <span v-if="approveSelected"><v-icon left class="mr-2">mdi-check</v-icon>Approved</span>
                  <span v-else>Approve</span>
                </v-btn>
                <v-btn large :outlined="!rejectSelected" color="red" class="font-weight-bold white--text select-button" @click="selectReject()">
                  <span v-if="rejectSelected"><v-icon left class="mr-2">mdi-close</v-icon>Rejected</span>
                  <span v-else>Reject</span>
                </v-btn>
              </v-col>
              <v-col class="pb-0 text-right">
                <v-btn large depressed :loading="isSaving" :disabled="!canSelect" class="grey lighten-3 font-weight-bold" @click="saveSelection()">DONE</v-btn>
              </v-col>
            </v-row>

        </v-col>

        <!-- Account Status Column -->
        <v-col class="col-12 col-md-4 pa-6 pa-md-8">
          <h2 class="mb-5">Account Status</h2>
          <v-row>
            <v-col class="col-12 col-sm-5 py-2">Status</v-col>
            <v-col class="py-2">{{ statusLabel }}</v-col>
          </v-row>
          <v-row>
            <v-col class="col-12 col-sm-5 py-2">
              <span v-if="accountUnderReview.statusCode === 'ACTIVE'">Approved By</span>
              <span v-if="accountUnderReview.statusCode === 'REJECTED'">Rejected By</span>
            </v-col>
            <v-col class="py-2">
              {{ accountUnderReviewAffidavitInfo.decisionMadeBy }}<br/>
              {{ formatDate(accountUnderReviewAffidavitInfo.decisionMadeOn) }}
            </v-col>
          </v-row>
          <v-row>
            <v-col class="col-12 col-sm-5 py-2">Created On</v-col>
            <v-col class="py-2">{{ formatDate(accountUnderReview.created) }}</v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Account, AccountStatus } from '@/util/constants'
import { MembershipType, Organization } from '@/models/Organization'
import { mapActions, mapGetters, mapState } from 'vuex'
import { Address } from '@/models/address'
import { AffidavitInformation } from '@/models/affidavit'
import Component from 'vue-class-component'
import { Contact } from '@/models/contact'
import DocumentService from '@/services/document.services'
import OrgService from '@/services/org.services'
import { Prop } from 'vue-property-decorator'
import StaffModule from '@/store/modules/staff'
import { User } from '@/models/user'
import Vue from 'vue'
import { getModule } from 'vuex-module-decorators'
import moment from 'moment'

@Component({
  computed: {
    ...mapState('staff', ['accountUnderReview', 'accountUnderReviewAddress', 'accountUnderReviewAdmin', 'accountUnderReviewAdminContact', 'accountUnderReviewAffidavitInfo']),
    ...mapGetters('staff', ['accountNotaryName', 'accountNotaryContact', 'affidavitDocumentUrl'])
  },
  methods: {
    ...mapActions('staff', ['syncAccountUnderReview', 'approveAccountUnderReview', 'rejectAccountUnderReview'])
  }
})
export default class ReviewAccountView extends Vue {
  @Prop() orgId: number
  private staffStore = getModule(StaffModule, this.$store)
  private isLoading = true
  private isSaving = false
  private approveSelected = false
  private rejectSelected = false
  private readonly accountUnderReview!: Organization
  private readonly accountUnderReviewAddress!: Address
  private readonly accountUnderReviewAdmin!: User
  private readonly accountUnderReviewAdminContact!: Contact
  private readonly accountUnderReviewAffidavitInfo!: AffidavitInformation
  private readonly accountNotaryName!: string
  private readonly accountNotaryContact!: Contact
  private readonly affidavitDocumentUrl!: string
  private readonly syncAccountUnderReview!: (organizationIdentifier: number) => Promise<void>
  private readonly approveAccountUnderReview!: () => Promise<void>
  private readonly rejectAccountUnderReview!: () => Promise<void>

  private get canSelect (): boolean {
    return this.accountUnderReview.statusCode === AccountStatus.PENDING_AFFIDAVIT_REVIEW
  }

  private get statusLabel (): string {
    switch (this.accountUnderReview.statusCode) {
      case AccountStatus.ACTIVE:
        return 'Approved'
      case AccountStatus.REJECTED:
        return 'Rejected'
      case AccountStatus.PENDING_AFFIDAVIT_REVIEW:
        return 'Pending'
      default:
        return ''
    }
  }

  private formatDate (date: Date): string {
    return moment(date).format('MMM DD, YYYY')
  }

  private async mounted () {
    await this.syncAccountUnderReview(this.orgId)

    // Set initial approved/rejected status based on current account
    switch (this.accountUnderReview.statusCode) {
      case AccountStatus.ACTIVE:
        this.approveSelected = true
        break
      case AccountStatus.REJECTED:
        this.rejectSelected = true
        break
      default:
        break
    }

    this.isLoading = false
  }

  private async downloadAffidavit (): Promise<void> {
    // Invoke document service to get affidavit for current organization
    DocumentService.getSignedAffidavit(this.affidavitDocumentUrl, `${this.accountUnderReview.name}-affidavit`)
  }

  private selectApprove (): void {
    if (this.canSelect) {
      this.approveSelected = true
      this.rejectSelected = false
    }
  }

  private selectReject (): void {
    if (this.canSelect) {
      this.approveSelected = false
      this.rejectSelected = true
    }
  }

  private async saveSelection (): Promise<void> {
    this.isSaving = true
    if (this.approveSelected) {
      await this.approveAccountUnderReview()
    } else if (this.rejectSelected) {
      await this.rejectAccountUnderReview()
    }
    this.$router.push('/searchbusiness')
  }

  private goBack (): void {
    this.$router.push('/searchbusiness')
  }
}
</script>

<style lang="scss" scoped>
  .main-col {
    border-color: lightgray;
    border-right-style: solid;
    border-right-width: 1px;
  }

  // BC Online Account Information
  .bcol-acc__name {
    font-size: 1.125rem;
    font-weight: 700;
  }

  .bcol-acc__meta {
    margin: 0;
    padding: 0;
    list-style-type: none;

    li {
      position: relative;
      display: inline-block
    }

    li + li {
      &:before {
        content: ' | ';
        display: inline-block;
        position: relative;
        top: -2px;
        left: 2px;
        width: 2rem;
        vertical-align: top;
        text-align: center;
      }
    }
  }

  .mailing-address {
    list-style-type: none;
    margin: 0;
    padding: 0;
  }

  .select-button {
    width: 8.75rem;
  }
</style>